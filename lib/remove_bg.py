from rembg import remove
from PIL import Image
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor

import onnxruntime as ort

def process_images_in_batch(batch, use_gpu):
    """
    Process a batch of images: remove their backgrounds and save the results.

    Args:
    batch (list): List of tuples (input_path, output_path).
    use_gpu (bool): Whether to enable GPU support.

    Returns:
    int: Number of images successfully processed in this batch.
    """
    success_count = 0
    for input_path, output_path in batch:
        try:
            with Image.open(input_path) as img:
                # Initialize ONNX session options with GPU support if required
                session_options = ort.SessionOptions()
                providers = ["CUDAExecutionProvider"] if use_gpu else ["CPUExecutionProvider"]
                ort.set_default_logger_severity(3)  # Suppress non-critical logging

                # Initialize the rembg remove function with appropriate providers
                output = remove(img, session_options=session_options, providers=providers)
                output.save(output_path)
            success_count += 1
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")
    return success_count

def remove_bg_from_files_in_dir(directory, max_workers=2, batch_size=3, use_gpu=False):
    """
    Process all JPG, JPEG, and PNG images in the given directory and its subfolders using parallel processing and GPU.

    Args:
    directory (str): Path to the directory containing images.
    max_workers (int): Maximum number of threads to use for parallel processing.
    batch_size (int): Number of images to process per batch.
    use_gpu (bool): Whether to enable GPU support.

    Returns:
    int: The number of images successfully processed.
    """
    files_to_process = []

    # Gather all the image files to process
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(subdir, file)
                output_filename = os.path.splitext(file)[0] + '.png'
                output_path = os.path.join(subdir, output_filename)
                files_to_process.append((input_path, output_path))

    processed_count = 0

    # Divide files into batches
    batches = [files_to_process[i:i + batch_size] for i in range(0, len(files_to_process), batch_size)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=len(files_to_process), desc="Removing Backgrounds", unit="image") as pbar:
            futures = {
                executor.submit(process_images_in_batch, batch, use_gpu): batch
                for batch in batches
            }

            for future in futures:
                processed_count += future.result()
                pbar.update(len(futures[future]))

    return processed_count
