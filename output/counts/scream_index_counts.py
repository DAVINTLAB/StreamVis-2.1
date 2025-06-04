import json
import os

def scream_index_mean(json_file_path):
    """ Calculate the mean Scream Index from a JSON file.
    This function reads a JSON file containing objects with a 'scream_index' field,
    calculates the mean of these indices, and prints the result.
    """
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    scream_indices = [obj['scream_index'] for obj in data if 'scream_index' in obj]
    if scream_indices:
        return sum(scream_indices) / len(scream_indices)
    return 0.0

    