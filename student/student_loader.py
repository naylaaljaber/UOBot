import json

def load_student_data(path):
    """Loads student data from the given JSON path."""
    with open(path, 'r') as f:
        return json.load(f)

