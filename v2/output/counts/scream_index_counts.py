import json
import os

def scream_index_mean(data):
    """ Calculate the mean Scream Index from a JSON file.
    This function reads a JSON file containing objects with a 'scream_index' field,
    calculates the mean of these indices, and prints the result.
    """
    scream_indices = [obj['scream_index'] for obj in data if 'scream_index' in obj]
    if scream_indices:
        return sum(scream_indices) / len(scream_indices)
    return 0.0

    