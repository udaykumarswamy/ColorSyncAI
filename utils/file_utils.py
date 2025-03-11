import json

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

def load_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)