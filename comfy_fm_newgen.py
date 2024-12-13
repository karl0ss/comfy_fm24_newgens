import argparse
import os
import random
import json
import configparser
import pycountry
import inflect
import logging
import sys

from tqdm import tqdm
from lib.rtf_parser import RTF_Parser
from lib.remove_bg import remove_bg_from_files_in_dir
from lib.generate_xml import create_config_xml
from lib.resize_images import resize_images
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Load user configurations
user_config = configparser.ConfigParser()
user_config.read("config.cfg")

rtf = RTF_Parser()
p = inflect.engine()

output_folder = user_config["general"]["output_dir"]


def generate_image(uid, comfy_prompt, model, steps):
    """Generate an image using the Comfy API."""
    url = user_config["general"]["url"]

    # Initialize API and workflow
    api = ComfyApiWrapper(url)
    wf = ComfyWorkflowWrapper("./workflow_api.json")

    # Set workflow parameters
    wf.set_node_param("KSampler", "seed", random.getrandbits(32))
    wf.set_node_param("KSampler", "steps", steps)
    wf.set_node_param("positive", "text", comfy_prompt)
    wf.set_node_param("Save Image", "filename_prefix", uid)
    wf.set_node_param("Load Checkpoint", "ckpt_name", model)

    # queue your workflow for completion
    results = api.queue_and_wait_images(wf, "Save Image")
    for filename, image_data in results.items():
        with open(f"./generated_images/{uid}.png", "wb+") as f:
            f.write(image_data)


def get_country_name_from_code(code):
    """Get country name from 3-letter ISO code."""
    try:
        country = pycountry.countries.get(alpha_3=code.upper())
        return country.name if country else "Unknown country code"
    except KeyError:
        return "Invalid country code"


def generate_prompts_for_players(players, app_config):
    """Generate images for a specific player and configuration."""
    prompts = []
    for player in players:
        print(f"\nGenerating image for {player[0]} - {player[8]}")
        os.makedirs(output_folder, exist_ok=True)

        country = get_country_name_from_code(player[1])
        facial_characteristics = random.choice(app_config["facial_characteristics"])
        hair_length = app_config["hair_length"][player[5]]
        hair_colour = app_config["hair_color"][player[6]]
        skin_tone = app_config["skin_tone_map"][player[7]]
        player_age = p.number_to_words(player[3])
        hair = random.choice(app_config["hair"])

        # Format the prompt
        prompt = app_config["prompt"].format(
            skin_tone=skin_tone,
            age=player_age,
            country=country,
            facial_characteristics=facial_characteristics or "no facial hair",
            hair=f"{hair_length} {hair_colour} {hair}",
        )
        print(f"Generated prompt: {prompt}")
        prompt = f"{player[0]}:{prompt}"
        prompts.append(prompt)
    return prompts


def main():
    """Main function for generating images."""
    parser = argparse.ArgumentParser(description="Generate images for country groups")
    parser.add_argument(
        "--rtf_file",
        type=str,
        default=None,
        help="Path to the RTF file to be processed",
    )
    parser.add_argument(
        "--num_inference_steps",
        type=int,
        default=6,
        help="Number of inference steps. Defaults to 6",
    )
    args = parser.parse_args()

    if not args.rtf_file:
        raise Exception("Please pass in a RTF file as --rtf_file")

    # Parse the RTF file
    rtf_file = rtf.parse_rtf(args.rtf_file)[:5]

    # Extract unique values
    hair_length = list(set(item[5] for item in rtf_file))
    hair_colour = list(set(item[6] for item in rtf_file))
    skin_tone = list(set(item[7] for item in rtf_file))

    # Load configurations
    with open("config.json", "r") as f:
        app_config = json.load(f)
    print(f"{len(rtf_file)} images will be generated")
    prompts = generate_prompts_for_players(rtf_file, app_config)
    for prompt in tqdm(prompts, desc="Generating Images"):
        uid = prompt.split(":")[0]
        comfy_prompt = prompt.split(":")[1]
        generate_image(
            uid,
            comfy_prompt,
            user_config["general"]["model"],
            args.num_inference_steps
        )
    remove_bg_from_files_in_dir(output_folder)
    resize_images(output_folder)
    create_config_xml(output_folder)
    print("\nImage generation complete for players in RTF file.")


if __name__ == "__main__":
    main()
