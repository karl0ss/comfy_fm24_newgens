import os
from PIL import Image
from tqdm import tqdm


def resize_images(folder_path):
    # Loop through all files in the folder
    for filename in tqdm(os.listdir(folder_path), desc="Resizing Images"):
        # Check if the file is a PNG image
        if filename.endswith('.png'):
            # Full path to the image file
            image_path = os.path.join(folder_path, filename)
            # Open the image file
            with Image.open(image_path) as img:
                # Resize the image to 256x256
                img_resized = img.resize((256, 256))
                img_resized.save(os.path.join(folder_path, filename))