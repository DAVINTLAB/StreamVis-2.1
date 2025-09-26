import json
from collections import defaultdict

def count_toxic_types(data):
    """
    Counts occurrences of each toxic type from a JSON file.

    Args:
        data (list [dict]): JSON data with comments.

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

    for item in data:
        for toxic_type, index in item.items():
            if toxic_type in toxic_types and index > 0.7:  # Only count toxic types with index above 0.7
                toxic_types_count[toxic_type] += 1

    return dict(toxic_types_count)
