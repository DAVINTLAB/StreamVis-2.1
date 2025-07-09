import json

def get_all_toxic_type_count(json_file_path: str = 'v1/input/comments.json'):
    """
    Counts occurrences of each toxic type from a JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file containing toxic indexes.
        
    Returns:
        dict: A dictionary with toxic types as keys and their counts as values.
    """
    toxic_types = {
        'toxicity': 0,
        'severe_toxicity': 0,
        'obscene': 0,
        'identity_attack': 0,
        'insult': 0,
        'threat': 0,
        'sexual_explicit': 0
    }

    toxic_types_count = 0

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            for toxic_type in toxic_types.keys():
                if item.get(toxic_type, 0) > 0.7:  # Only count toxic types with index above 0.7
                    toxic_types_count += 1
                    break

    return toxic_types_count/data.__len__() if data else 0.0