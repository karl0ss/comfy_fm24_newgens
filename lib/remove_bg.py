from rembg import remove
from PIL import Image
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
import onnxruntime as ort

def process_images_in_batch(batch, directory, use_gpu):
    """
    Process a batch of images: remove their backgrounds and save the results.

    Args:
    batch (list): List of filenames to process (without path or extension).
    directory (str): Base directory to locate input files.
    use_gpu (bool): Whether to enable GPU support.

    Returns:
    int: Number of images successfully processed in this batch.
    """
    success_count = 0
    for filename in batch:
        input_path = os.path.join(directory, f"{filename}.png")
        output_path = os.path.join(directory, f"{filename}.png")

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

def remove_bg_from_file_list(directory, filenames, max_workers=2, batch_size=2, use_gpu=False):
    """
    Process a list of specified filenames: remove their backgrounds and save the results.

    Args:
    directory (str): Path to the directory containing images.
    filenames (list): List of filenames (without path or extension) to process.
    max_workers (int): Maximum number of threads to use for parallel processing.
    batch_size (int): Number of images to process per batch.
    use_gpu (bool): Whether to enable GPU support.

    Returns:
    int: The number of images successfully processed.
    """
    processed_count = 0

    # Divide filenames into batches
    batches = [filenames[i:i + batch_size] for i in range(0, len(filenames), batch_size)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=len(filenames), desc="Removing Backgrounds", unit="image") as pbar:
            futures = {
                executor.submit(process_images_in_batch, batch, directory, use_gpu): batch
                for batch in batches
            }

            for future in futures:
                processed_count += future.result()
                pbar.update(len(futures[future]))

    return processed_count