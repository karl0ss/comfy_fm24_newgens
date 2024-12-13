import os
from rembg import remove
from PIL import Image
from tqdm import tqdm

def remove_bg_from_files_in_dir(directory):
    """
    Process all JPG and JPEG images in the given directory and its subfolders.

    Args:
    directory (str): Path to the directory containing images.

    Returns:
    int: The number of images successfully processed.
    """
    processed_count = 0
    
    # Get the total number of files to process
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    
    # Create a progress bar
    with tqdm(total=total_files, desc="Processing images", unit="image") as pbar:
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', 'png')):
                    input_path = os.path.join(subdir, file)
                    output_filename = os.path.splitext(file)[0] + '.png'
                    output_path = os.path.join(subdir, output_filename)
                    
                    try:
                        with Image.open(input_path) as img:
                            output = remove(img)
                            output.save(output_path)
                        processed_count += 1
                    except Exception as e:
                        print(f"Error processing {input_path}: {str(e)}")
                
                # Update the progress bar
                pbar.update(1)
    
    return processed_count