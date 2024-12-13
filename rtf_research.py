import sys
from lib.rtf_parser import RTF_Parser

rtf = RTF_Parser()

# Parse the RTF file
try:
    rtf_file = rtf.parse_rtf("./Gen.rtf")
except FileNotFoundError:
    print("Error: RTF file not found.")
    sys.exit(1)

# Extract unique values with examples
try:
    unique_hair_length = {}
    unique_hair_colour = {}
    unique_skin_tone = {}

    for item in rtf_file:
        try:
            uid = item[0]
            name = item[8]
            hair_length = item[5]
            hair_colour = item[6]
            skin_tone = item[7]

            # Add examples for unique hair lengths
            if hair_length not in unique_hair_length:
                unique_hair_length[hair_length] = []
            if len(unique_hair_length[hair_length]) < 3:
                unique_hair_length[hair_length].append({"UID": uid, "Name": name})

            # Add examples for unique hair colours
            if hair_colour not in unique_hair_colour:
                unique_hair_colour[hair_colour] = []
            if len(unique_hair_colour[hair_colour]) < 3:
                unique_hair_colour[hair_colour].append({"UID": uid, "Name": name})

            # Add examples for unique skin tones
            if skin_tone not in unique_skin_tone:
                unique_skin_tone[skin_tone] = []
            if len(unique_skin_tone[skin_tone]) < 3:
                unique_skin_tone[skin_tone].append({"UID": uid, "Name": name})

        except IndexError:
            continue  # Skip rows with missing columns

    # Print sorted results
    print("Hair Lengths with examples (sorted):")
    for length in sorted(unique_hair_length.keys()):
        print(f"{length}: {unique_hair_length[length]}")

    print("\nHair Colours with examples (sorted):")
    for colour in sorted(unique_hair_colour.keys()):
        print(f"{colour}: {unique_hair_colour[colour]}")

    print("\nSkin Tones with examples (sorted):")
    for tone in sorted(unique_skin_tone.keys()):
        print(f"{tone}: {unique_skin_tone[tone]}")

except Exception as e:
    print(f"An error occurred: {e}")