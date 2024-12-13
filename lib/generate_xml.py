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
