def validate_age_range(age_range):
    if age_range is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        age_range = int(age_range)
    except:
        raise ValueError("Invalid age range: age range need to be 0, 1, 2, 3 or 4")
    if (age_range > 4 or age_range < 0):
        raise ValueError("Invalid age range: age range need to be 0, 1, 2, 3 or 4")
    return age_range

def validate_age_string(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")
    valid_age_values = {"Adult", "Child", "Student", "Senior"}
    if value not in valid_age_values:
        raise ValueError("Age must be one of: Adult, Child, Student, Senior.")
    return value


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

def validate_price(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        value = float(value)
    except:
        raise ValueError("Price/quantity needs to be integer/floating point")
    if value < 0:
        raise ValueError("Price/quantity must be non-negative.")
    return value

def validate_null(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")

def validate_year(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        value = int(value)
    except:
        raise ValueError("Year needs to be integer")
    if value < 0:
        raise ValueError("Must be valid year")
    return value


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