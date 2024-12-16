import os
import shutil
from pathlib import Path


def copy_folders_to_my_documents():
    # Get the current script's directory
    script_dir = Path(__file__).parent.resolve()

    # Get the "My Documents" folder
    my_documents = Path.home() / "Documents"

    # Define the target folder (KARL TEST)
    target_folder = my_documents / f"Sports Interactive/Football Manager 2024" 

    # Create the target folder if it doesn't exist
    target_folder.mkdir(parents=True, exist_ok=True)

    # Define the source folders
    source_folders = ["views", "filters"]

    for folder in source_folders:
        source_path = script_dir / folder
        target_path = target_folder / folder

        if source_path.exists() and source_path.is_dir():
            # Copy the folder and merge contents
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
            print(f"Copied '{folder}' to '{target_path}'")
        else:
            print(f"Source folder '{folder}' does not exist. Skipping.")


if __name__ == "__main__":
    copy_folders_to_my_documents()
