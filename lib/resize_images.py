import os
from PIL import Image
from tqdm import tqdm


def resize_images(folder_path, processed_players):
    # Loop through all files in the folder
    for player in tqdm(processed_players, desc="Resizing Images"):
        player = f"{player}.png"
        # Full path to the image file
        image_path = os.path.join(folder_path, player)
        # Open the image file
        with Image.open(image_path) as img:
            # Resize the image to 256x256
            img_resized = img.resize((256, 256))
            img_resized.save(os.path.join(folder_path, player))