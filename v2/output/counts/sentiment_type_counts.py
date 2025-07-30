import json
from collections import defaultdict

def count_sentiment_types(file_path):
    """
    Counts occurrences of each sentiment type from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing sentiment classifications.

    Returns:
        dict: A dictionary with sentiment types as keys and their counts as values.
    """
    sentiment_types_count = defaultdict(int)

    sentiment_types = [
        'NEU',
        'POS',
        'NEG'
    ]

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            sentiment = item['sentiment']
            sentiment_types_count[sentiment] += 1

    return dict(sentiment_types_count)
