"""
"""
from lib.rtf_parser import RTF_Parser
import aiohttp
import asyncio
import json
from PIL import Image
from io import BytesIO
import os
import random
import json
import pycountry
import inflect
import configparser
import argparse

user_config = configparser.ConfigParser()
user_config.read('config.cfg')

rtf = RTF_Parser()
p = inflect.engine()


async def generate_image(session, prompt, num_inference_steps, model):
    import random

    payload = json.dumps(
        {
            "prompt": {
                "3": {
                    "class_type": "KSampler",
                    "inputs": {
                        "cfg": 1.5,
                        "denoise": 1,
                        "latent_image": ["5", 0],
                        "model": ["4", 0],
                        "negative": ["7", 0],
                        "positive": ["6", 0],
                        "sampler_name": "dpmpp_2m_sde",
                        "scheduler": "karras",
                        "seed": random.getrandbits(32),
                        "steps": num_inference_steps,
                    },
                },
                "4": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": model},
                },
                "5": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {"batch_size": 1, "height": 512, "width": 512},
                },
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "clip": ["4", 1],
                        "text": prompt,
                    },
                },
                "7": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "clip": ["4", 1],
                        "text": "(nsfw, naked, nude, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation",
                    },
                },
                "8": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                },
                "9": {
                    "class_type": "SaveImage",
                    "inputs": {"filename_prefix": "FM", "images": ["8", 0]},
                },
            }
        }
    )
    url = user_config["general"]["url"]
    url = f"{url}prompt"
    headers = {"Content-Type": "application/json"}
    async with session.post(url, headers=headers, data=payload) as response:
        if response.status == 200:
            # response_data = await response.json()
            # image_data = response_data["images"][0].split(",")[1]
            # image_bytes = base64.b64decode(image_data)
            # return image_bytes
            pass
        else:
            return None


# def save_image(image_bytes, folder, filename, resize=False):
#     if image_bytes:
#         os.makedirs(folder, exist_ok=True)
#         full_path = os.path.join(folder, filename)

#         # Open the image using PIL
#         image = Image.open(BytesIO(image_bytes))

#         # Resize the image if the resize option is True
#         if resize:
#             image = image.resize((256, 256), Image.LANCZOS)

#         # Save the image
#         image.save(full_path)
#         print(f"Image saved as {full_path}")
#     else:
#         print("Failed to generate or save the image.")


def get_country_name_from_code(code):
    try:
        country = pycountry.countries.get(alpha_3=code.upper())
        return country.name if country else "Unknown country code"
    except KeyError:
        return "Invalid country code"
    

async def generate_images_for_country_group(
    session,
    player,
    config,
    model,
):
    print(f"\nGenerating image for {player[0]} - {player[8]}")
    folder_name = f"generated_images/"
    os.makedirs(folder_name, exist_ok=True)

    tasks = []
    for i in range(1):
        country = get_country_name_from_code(player[1])
        facial_characteristics = random.choice(config["facial_characteristics"])
        hair_length = config["hair_length"][player[5]]
        hair_colour = config["hair_color"][player[6]]
        skin_tone = config["skin_tone_map"][player[7]]
        player_age = p.number_to_words(player[3])
        hair = random.choice(config["hair"])

        prompt = config["prompt"].format(
            skin_tone=skin_tone,
            age=player_age,
            country=country,
            facial_characteristics=(
                facial_characteristics if facial_characteristics else "no facial hair"
            ),
            hair=f"{hair_length} {hair_colour} {hair}",
        )

        print(f"Generated prompt: {prompt}")

        task = asyncio.create_task(
            generate_image(
                session=session,
                prompt=prompt,
                num_inference_steps=6,
                model=model,
            )
        )
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    # for i, image_bytes in enumerate(image_bytes_list):
    #     if image_bytes:
    #         next_number = get_next_image_number(folder_name)
    #         file_name = f"{country_group}{next_number}.png"
    #         save_image(image_bytes, folder_name, file_name, resize)

    # return len([img for img in image_bytes_list if img is not None])


async def main():
    parser = argparse.ArgumentParser(description="Generate images for country groups")
    parser.add_argument("--rtf_file", type= str, default=None, help= "Path to the rtf file to be processed")
    parser.add_argument("--num_inference_steps", type=int, default=6, help="Number of inference steps. Defaults to 1")

    args = parser.parse_args()
    if not args.rtf_file:
        raise Exception("Please pass in a RTF file as --rtf_file")
    rtf_file = rtf.parse_rtf(args.rtf_file)
    
    # Extract unique values from positions 5, 6, and 7
    hair_length = list(
        set(item[pos] for item in rtf_file for pos in [5])
    )
    hair_colour = list(
            set(item[pos] for item in rtf_file for pos in [6])
        )
    skin_tone = list(
            set(item[pos] for item in rtf_file for pos in [7])
        )

    with open("config.json", "r") as f:
        app_config = json.load(f)

    total_images = len(rtf_file)
    # if not ask_user_confirmation(total_images, total_cost):
    #     print("Operation cancelled by user.")
    #     sys.exit(0)

    generated_images = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for player in rtf_file[:500]:
            task = asyncio.create_task(
                generate_images_for_country_group(
                    session,
                    player,
                    app_config,
                    user_config["general"]["model"],
                )
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        # generated_images = sum(results)

    print("\nImage generation complete for all country groups.")
    print(f"Total images generated: {generated_images}")


if __name__ == "__main__":
    asyncio.run(main())
