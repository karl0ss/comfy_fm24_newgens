import os
from rembg import remove
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def process_image(input_path, output_path):
    """
    Process a single image: remove its background and save the result.
    
    Args:
    input_path (str): Path to the input image.
    output_path (str): Path to save the processed image.
    
    Returns:
    bool: True if the image was successfully processed, False otherwise.
    """
    try:
        with Image.open(input_path) as img:
            output = remove(img)
            output.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False

def remove_bg_from_files_in_dir(directory, max_workers=2):
    """
    Process all JPG, JPEG, and PNG images in the given directory and its subfolders using parallel processing.

    Args:
    directory (str): Path to the directory containing images.
    max_workers (int): Maximum number of threads to use for parallel processing.
    
    Returns:
    int: The number of images successfully processed.
    """
    processed_count = 0
    files_to_process = []

    # Gather all the image files to process
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', 'png')):
                input_path = os.path.join(subdir, file)
                output_filename = os.path.splitext(file)[0] + '.png'
                output_path = os.path.join(subdir, output_filename)
                files_to_process.append((input_path, output_path))

    # Use ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use tqdm to show progress
        with tqdm(total=len(files_to_process), desc="Processing images", unit="image") as pbar:
            futures = {executor.submit(process_image, input_path, output_path): (input_path, output_path) for input_path, output_path in files_to_process}

            for future in futures:
                if future.result():
                    processed_count += 1
                pbar.update(1)

    return processed_count
