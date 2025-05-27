def toxic_types_filter(dict_data: list, toxic_type: str) -> list:
    """
    Filters the toxic types data based on the selected toxic type.

    Args:
        dict_data (dict): A dictionary containing messages and their toxic type indexes.
        toxic_type (str): The toxic type to filter by.

    Returns:
        dict: A dictionary containing all the messages above the toxic type index
    """
    
    dict_filtered = []

    toxic_type = toxic_type.lower().replace(' ', '_')

    for item in dict_data:
        if item[toxic_type] > 0.7:
            dict_filtered.append(item)

    print(f"Filtered data for {toxic_type}: {dict_filtered.__len__()} items")
    return dict_filtered
    