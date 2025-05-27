# Given a JSON file with toxic indexes, i want to count the occurrences of each toxic type (above 0.7 index) and return a dictionary with the counts.
import json
from collections import defaultdict

def count_toxic_types(file_path):
    """
    Counts occurrences of each toxic type from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing toxic indexes.

    Returns:
        dict: A dictionary with toxic types as keys and their counts as values.
    """
    toxic_types_count = defaultdict(int)

    toxic_types = [
        'toxicity',
        'severe_toxicity',
        'obscene',
        'identity_attack',
        'insult',
        'threat',
        'sexual_explicit'
    ]

    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            for toxic_type, index in item.items():
                if toxic_type in toxic_types and index > 0.7:  # Only count toxic types with index above 0.7
                    toxic_types_count[toxic_type] += 1

    return dict(toxic_types_count)