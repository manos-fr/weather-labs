import json

#Yedantra please refactor with your code i added to test teh main
def get_data(file_path):
    """Lload from users.JSON file."""
    with open(file_path, 'r') as data_file:
        return json.load(data_file)

def save_data(file_path, data):
    """save to users.JSON file."""
    with open(file_path, 'w') as data_file:
        json.dump(data, data_file, indent=4)