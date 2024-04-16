def validate_age_range(age_range):
    try:
        age_range = int(age_range)
    except:
        raise ValueError("Invalid age range: age range need to be 0, 1, 2, 3 or 4")
    if (age_range > 4 or age_range < 0):
        raise ValueError("Invalid age range: age range need to be 0, 1, 2, 3 or 4")
    return age_range



def validate_binary_encodings(num, name=None):
    try:
        num = int(num)
    except:
        if name is None:
            raise ValueError("There is a variable that is supposed to be 0 or 1. Please check and try again")
        raise ValueError(f"{name} needs to be either 0 or 1")
    if (num != 0 and num != 1):
        raise ValueError(f"{name} needs to be either 0 or 1")
    return num

def check_json_keys(request_json, key_set):
    """
    Function to check if the keys in the request.json object match the keys in the given set.

    Parameters:
    - request_json (dict): The JSON object obtained from Flask's request.json() method.
    - key_set (set): The set of keys to compare against.

    Returns:
    - bool: True if the keys in the JSON object match the keys in the set, False otherwise.
    """

    # Get the keys from the JSON object
    json_keys = set(request_json.keys())

    # Check if the keys in the JSON object match the keys in the set
    if json_keys == key_set:
        return True
    else:
        return False