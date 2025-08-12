def get_sentiments_peak(sentiment: str, dict_data: dict) -> list:
    """
    Get the peaks of sentiment over time.

    Args:
        sentiment (str): The sentiment to analyze (e.g., "positive", "negative").
        dict_data (dict): A dictionary containing timestamps and their corresponding sentiment values.

    Returns:
        dict: A dictionary with timestamps as keys and sentiment values as values for the peaks.
    """
    min_time = dict_data[0]["time_in_seconds"]
    max_time = dict_data[-1]["time_in_seconds"]

    # Creates peaks of 5 minutes
    peaks = []

    start_time = min_time
    while start_time < max_time:
        end_time = start_time + 300
        peak = {
            "start_time": start_time,
            "end_time": end_time,
            "sentiment": 0,
            "count": 0
        }
        for entry in dict_data:
            if start_time <= entry["time_in_seconds"] < end_time:
                if(entry["sentiment"] == sentiment):
                    peak["sentiment"] += 1
                peak["count"] += 1
        peak["start_time"] = start_time
        peak["end_time"] = end_time
        start_time = end_time
        peaks.append(peak)

    print(f"Peaks found: {peaks}")
    # Returns the 5 highest peaks
    highest_peaks = sorted(peaks, key=lambda x: x["sentiment"]/x["count"], reverse=True)[:5]
    print(f"Highest peaks: {highest_peaks}")
    return highest_peaks
