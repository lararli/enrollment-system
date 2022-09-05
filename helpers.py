import json
import os

def create_id(file_name, entity, field):
    """
    Create unique IDs for the entities (users and courses).
    """
    max_value = 0
    file_data = load(file_name)
    for item in file_data[entity]:
        num = item[field]
        if num >= max_value:
            max_value = num
    new_id = max_value + 1
    return new_id


def load(file_path):
    with open(file_path, "r+") as f:
        resp = json.load(f)
    return resp

def clear_screen():
    return os.system('cls' if os.name == 'nt' else 'clear')