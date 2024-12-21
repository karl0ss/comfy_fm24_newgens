import configparser

def list_profiles(cfg_file):
    config = configparser.ConfigParser()
    config.read(cfg_file)
    
    profiles = [section.split(':', 1)[1] for section in config.sections() if section.startswith('profile:')]
    return profiles


def choose_profile(cfg_file):
    profiles = list_profiles(cfg_file)
    if not profiles:
        print("No profiles found.")
        return None

    print("Available Profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile}")

    while True:
        try:
            choice = int(input("Enter the number of the profile you want to use: "))
            if 1 <= choice <= len(profiles):
                return profiles[choice - 1]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
def create_or_update():
    values = ["Create", "Update"]
    print("Create or Update:")
    for i, profile in enumerate(values, 1):
        print(f"{i}. {profile}")

    while True:
        try:
            choice = int(input("Enter the number of the choice: "))
            if 1 <= choice <= len(values):
                if choice == 1:
                    return False
                else:
                    return True
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")          
            
            
def process_player_or_file():
    values = ["Whole File", "Specific Player"]
    print("Process whole rtf file or a specific player?:")
    for i, profile in enumerate(values, 1):
        print(f"{i}. {profile}")

    while True:
        try:
            choice = int(input("Enter the number of the choice: "))
            if 1 <= choice <= len(values):
                if choice == 1:
                    return False
                else:
                    return True
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")          
            
                        
def get_player_input():
    # Prompt the user to enter a UUID
    player_uuid = input("Please enter the player UUID: ").strip()

    # Validate that the UUID is not empty
    while not player_uuid:
        print("Player UUID cannot be empty. Please try again.")
        player_uuid = input("Please enter the player UUID: ").strip()

    return int(player_uuid)