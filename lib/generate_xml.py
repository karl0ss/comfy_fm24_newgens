import os
import xml.etree.ElementTree as ET


def parse_or_create_xml(file_path, create_if_missing=True):
    """
    Parse an existing XML file or create a new one if it doesn't exist.
    """
    if os.path.exists(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
    elif create_if_missing:
        # Create a new XML structure if file doesn't exist
        root = ET.Element("record")
        tree = ET.ElementTree(root)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return tree, root


def get_or_create_maps_list(root):
    """
    Get the <list id="maps"> element or create it if it doesn't exist.
    """
    maps = root.find(".//list[@id='maps']")
    if maps is None:
        maps = ET.SubElement(root, "list", id="maps")
    return maps


def add_uid_to_maps(maps, uid, football_manager_version):
    """
    Add a UID to the maps list if it doesn't already exist.
    """
    if football_manager_version == "2024":
        prefix = "r-"
    else:
        prefix = ""
    for record in maps.findall("record"):
        if record.attrib.get("from") == str(uid):
            return  # UID already exists
    ET.SubElement(
        maps,
        "record",
        attrib={
            "from": str(uid),
            "to": f"graphics/pictures/person/{prefix}{uid}/portrait",
        },
    )


def update_player_file_list(folder_path, processed_players):
    """
    Updates each player in the list with the full file path and `.png` extension.

    Args:
        folder_path (str): The path to the folder where the player files are stored.
        processed_players (list): A list of player names to be updated.
    """
    for i in range(len(processed_players)):
        processed_players[i] = os.path.join(folder_path, f"{processed_players[i]}.png")
    return processed_players


def create_config_xml(folder_path, processed_players, football_manager_version):
    """
    Create a new config.xml file based on .png files in the folder.
    """
    # Prepare the XML structure
    root = ET.Element("record")
    ET.SubElement(root, "boolean", id="preload", value="false")
    ET.SubElement(root, "boolean", id="amap", value="false")
    maps = ET.SubElement(root, "list", id="maps")

    # Add records for each .png file
    for player in processed_players:
        add_uid_to_maps(maps, player, football_manager_version)

    # Save the XML file
    output_path = os.path.join(folder_path, "config.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Config XML created at: {output_path}")


def append_to_config_xml(folder_path, processed_players, football_manager_version):
    """
    Append new UIDs to an existing config.xml file.
    """
    file_path = os.path.join(folder_path, "config.xml")
    tree, root = parse_or_create_xml(file_path, create_if_missing=False)

    # Get the maps list
    maps = get_or_create_maps_list(root)

    # Add new UIDs
    for uid in processed_players:
        add_uid_to_maps(maps, uid, football_manager_version)

    # Save the updated XML file
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    print(f"Appended new UIDs to {file_path}")
