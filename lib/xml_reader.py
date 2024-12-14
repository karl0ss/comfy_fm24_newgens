import xml.etree.ElementTree as ET

def extract_from_values(xml_file):
    """
    Extract all 'from' values from the record elements in the XML file.

    Args:
    xml_file (str): Path to the XML file.

    Returns:
    list: List of all 'from' attribute values.
    """
    from_values = []
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all 'record' elements and extract 'from' attributes
    for record in root.findall(".//record"):
        from_value = record.get('from')
        if from_value:
            from_values.append(from_value)
    
    return from_values