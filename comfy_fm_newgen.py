import argparse
import os
import random
import json
import configparser
import pycountry
import inflect
import logging
import sys
import logging
import logging.config

from tqdm import tqdm
from lib.rtf_parser import RTF_Parser
from lib.remove_bg import remove_bg_from_file_list
from lib.generate_xml import create_config_xml, append_to_config_xml
from lib.resize_images import resize_images
from lib.xml_reader import extract_from_values
from lib.general import (
    choose_profile,
    create_or_update,
    process_player_or_file,
    get_player_input,
)
from lib.logging import LOGGING_CONFIG

# from simple_term_menu import TerminalMenu
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

logging.config.dictConfig(LOGGING_CONFIG)

cut = None
update = False
use_gpu = False
process_player = False

# Load user configurations
user_config = configparser.ConfigParser()
try:
    user_config.read("./user_config.cfg")
    selected_profile = choose_profile("./user_config.cfg")
    selected_profile = f"profile:{selected_profile}"
    output_folder = user_config[selected_profile]["output_dir"]
    logging.debug("Configuration loaded successfully.")
except KeyError as e:
    logging.error(f"Missing configuration key: {e}")
    sys.exit(1)

rtf = RTF_Parser()
p = inflect.engine()


def generate_image(uid, comfy_prompt):
    """Generate an image using the Comfy API."""
    try:
        # Initialize API and workflow
        api = ComfyApiWrapper(user_config["comfyui"]["comfyui_url"])
        wf = ComfyWorkflowWrapper("./workflow_api.json")

        # Set workflow parameters
        wf.set_node_param("KSampler", "seed", random.getrandbits(32))
        # wf.set_node_param("KSampler", "steps", steps)
        wf.set_node_param("positive", "text", comfy_prompt)
        wf.set_node_param("Save Image", "filename_prefix", uid)
        wf.set_node_param(
            "Load Checkpoint", "ckpt_name", user_config["comfyui"]["model"]
        )
        # Queue your workflow for completion
        logging.debug(f"Generating image for UID: {uid}")
        results = api.queue_and_wait_images(wf, "Save Image")
        for filename, image_data in results.items():
            with open(
                f"{user_config[selected_profile]['output_dir']}{uid}.png", "wb+"
            ) as f:
                f.write(image_data)
        logging.debug(f"Image generated successfully for UID: {uid}")
    except Exception as e:
        logging.error(f"Failed to generate image for UID: {uid}. Error: {e}")


def get_country_name(app_config, country_code):
    # First check if it's a custom mapping
    if country_code in app_config["facial_characteristics"]:
        return app_config["facial_characteristics"][country_code]

    # Use pycountry for standard country codes
    country = pycountry.countries.get(alpha_3=country_code)
    if country:
        return country.name
    return "Unknown Country"


def generate_prompts_for_players(players, app_config):
    """Generate images for a specific player and configuration."""
    prompts = []
    for player in players:
        try:
            logging.debug(f"Generating prompt for {player[0]} - {player[8]}")
            os.makedirs(output_folder, exist_ok=True)

            country = get_country_name(app_config, player[1])
            facial_characteristics = random.choice(app_config["facial_characteristics"])
            hair_length = app_config["hair_length"][player[5]]
            hair_colour = app_config["hair_color"][player[6]]
            skin_tone = app_config["skin_tone_map"][player[7]]
            player_age = p.number_to_words(player[3])
            if int(player[5]) > 1:
                hair_extra = random.choice(app_config["hair"])
            else:
                hair_extra = ""

            # Format the prompt
            prompt = app_config["prompt"].format(
                skin_tone=skin_tone,
                age=player_age,
                country=country,
                facial_characteristics=facial_characteristics or "no facial hair",
                hair=f"{hair_length} {hair_colour} {hair_extra}",
            )
            logging.debug(f"Generated prompt: {prompt}")
            prompt = f"{player[0]}:{prompt}"
            prompts.append(prompt)
        except KeyError as e:
            logging.warning(f"Key error while generating prompt for player: {e}")
    return prompts


def post_process_images(
    output_folder, update, processed_players, football_manager_version
):
    """
    Handles post-processing tasks for generated images.

    Args:
        output_folder (str): Path to the folder where images are stored.
        update (bool): Flag to determine if XML config should be updated.
        processed_players (list): List of processed player IDs.
    """
    try:
        # Resize images to desired dimensions
        resize_images(output_folder, processed_players)
        logging.debug("Images resized successfully.")

        # Remove background from images using GPU if available
        remove_bg_from_file_list(output_folder, processed_players, use_gpu=use_gpu)
        logging.debug("Background removed from images.")

        # Update or create configuration XML
        if update:
            append_to_config_xml(
                output_folder, processed_players, football_manager_version
            )
            logging.debug("Configuration XML updated.")
        else:
            create_config_xml(
                output_folder, processed_players, football_manager_version
            )
            logging.debug("Configuration XML created.")
    except Exception as e:
        logging.error(f"Post-processing failed: {e}")
        raise  # Re-raise the exception to ensure the script stops if post-processing fails.


def main():
    """Main function for generating images."""
    # parser = argparse.ArgumentParser(description="Generate images for country groups")
    # parser.add_argument(
    #     "--rtf_file",
    #     type=str,
    #     default=None,
    #     help="Path to the RTF file to be processed",
    # )
    # parser.add_argument(
    #     "--player_uuid",
    #     type=int,
    #     default=None,
    #     help="Player UUID to generate",
    # )
    # parser.add_argument(
    #     "--num_inference_steps",
    #     type=int,
    #     default=6,
    #     help="Number of inference steps. Defaults to 6",
    # )
    # args = parser.parse_args()

    # if not args.rtf_file:
    #     logging.error("Please pass in a RTF file as --rtf_file")
    #     sys.exit(1)

    # Load configurations
    try:
        with open("app_config.json", "r") as f:
            app_config = json.load(f)
        logging.debug("Application configuration loaded successfully.")
    except FileNotFoundError:
        logging.error("app_config.json file not found.")
        sys.exit(1)

    # Parse the RTF file
    try:
        # rtf_file = random.sample(rtf.parse_rtf(args.rtf_file), cut)
        rtf_location = user_config[selected_profile]["rtf_file"]
        rtf_file = rtf.parse_rtf(rtf_location)
        logging.info(f"Parsed RTF file successfully. Found {len(rtf_file)} players.")
    except FileNotFoundError:
        logging.error(f"RTF file not found: {rtf_location}")
        sys.exit(1)

    update = create_or_update()
    process_player = process_player_or_file()
    if process_player:
        player_uuid = get_player_input()
    # Check for processed
    try:
        if update:
            values_from_config = extract_from_values(
                f"{user_config[selected_profile]['output_dir']}config.xml"
            )
            # Extract the IDs from list_a
            ids_in_b = [item for item in values_from_config]

            # Filter list_a to remove inner lists whose first item matches an ID in list_b
            players_to_process = [item for item in rtf_file if item[0] not in ids_in_b]
            if process_player:
                players_to_process = [
                    inner_list
                    for inner_list in players_to_process
                    if int(inner_list[0]) == player_uuid
                ]
        elif process_player:
            players_to_process = [
                inner_list
                for inner_list in rtf_file
                if int(inner_list[0]) == player_uuid
            ]
        else:
            players_to_process = rtf_file
    except FileNotFoundError:
        logging.error("config.json file not found.")
        sys.exit(1)
    if len(players_to_process) > 0:
        print(f"Processing {len(players_to_process)} players")
        logging.info(f"Processing {len(players_to_process)} players")
        prompts = generate_prompts_for_players(players_to_process, app_config)
        for prompt in tqdm(prompts, desc="Generating Images"):
            uid = prompt.split(":")[0]
            comfy_prompt = prompt.split(":")[1]
            generate_image(uid, comfy_prompt)
        try:
            post_process_images(
                output_folder,
                update,
                [item[0] for item in players_to_process],
                user_config[selected_profile]["football_manager_version"],
            )
        except Exception as e:
            logging.error(f"Post-processing failed: {e}")
    else:
        print(f"{len(rtf_file)} players already processed")
        logging.info(f"{len(rtf_file)} players already processed")
    logging.info("Image generation complete for players in RTF file.")


if __name__ == "__main__":
    main()
