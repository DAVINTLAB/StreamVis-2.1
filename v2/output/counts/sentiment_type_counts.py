import json
from collections import defaultdict

def count_sentiment_types(data):
    """
    Counts occurrences of each sentiment type from a JSON file.

    Args:
        data (list[dict]): JSON data with comments

    Returns:
        dict: A dictionary with sentiment types as keys and their counts as values.
    """
    sentiment_types_count = defaultdict(int)

    sentiment_types = [
        'NEU',
        'POS',
        'NEG'
    ]

    for item in data:
        sentiment = item['sentiment']
        sentiment_types_count[sentiment] += 1

    return dict(sentiment_types_count)
