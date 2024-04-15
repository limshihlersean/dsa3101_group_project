from services.general_validator import validate_age_range, validate_binary_encodings, check_json_keys

def validate_tourist_volume(tourist_volume):
    try:
        tourist_volume = float(tourist_volume)
    except:
        raise ValueError("tourist volume need to be a valid number")
    if (tourist_volume < 0):
        raise ValueError("Invalid tourist volume: tourist volume per year must be more than 0")
    return tourist_volume

def validate_price_opt_data(data):
    if (not check_json_keys(data, {"age_range", "tourist_volume", "is_one_way", "is_citizen"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    age_range = validate_age_range(data["age_range"])
    tourist_volume = validate_tourist_volume(data["tourist_volume"])
    is_one_way = validate_binary_encodings(data["is_one_way"], name="is_one_way")
    is_citizen = validate_binary_encodings(data["is_citizen"], name="is_citizen")
    return age_range, tourist_volume, is_one_way, is_citizen