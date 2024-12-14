import os
import xml.etree.ElementTree as ET

def create_config_xml(folder_path):
    # Define the root element
    root = ET.Element("record")

    # Add resource manager options
    ET.SubElement(root, "boolean", id="preload", value="false")
    ET.SubElement(root, "boolean", id="amap", value="false")

    # Add the maps section
    maps = ET.SubElement(root, "list", id="maps")

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            # Extract the UID from the filename (remove the extension)
            uid = os.path.splitext(filename)[0]

            # Create a record for each file
            ET.SubElement(maps, "record", attrib={"from": uid, "to": f"graphics/pictures/person/r-{uid}/portrait"})

    # Create the XML tree
    tree = ET.ElementTree(root)

    # Save the XML file
    output_path = os.path.join(folder_path, "config.xml")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Config XML created at: {output_path}")


def append_to_config_xml(file_path, uid_list):
    # Check if the file exists
    file_path = f"{file_path}/config.xml"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Parse the existing XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the <list id="maps"> element
    maps = root.find(".//list[@id='maps']")
    if maps is None:
        raise ValueError("The XML file does not contain a <list id='maps'> element.")

    # Add new UIDs
    for uid in uid_list:
        # Check if the UID already exists (escaping 'from' in XPath)
        existing = None
        for record in maps.findall("record"):
            if record.attrib.get('from') == str(uid):
                existing = record
                break
        
        if existing is None:
            # Add the new record if the UID doesn't exist
            ET.SubElement(maps, "record", attrib={"from": str(uid), "to": f"graphics/pictures/person/r-{uid}/portrait"})

    # Write the updated XML back to the file
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    print(f"Appended new UIDs to {file_path}")