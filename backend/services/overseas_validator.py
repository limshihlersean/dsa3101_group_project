from services.general_validator import validate_age_range, validate_price, validate_binary_encodings, validate_null, check_json_keys


def validate_tourist_volume(tourist_volume):
    if tourist_volume is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        tourist_volume = float(tourist_volume)
    except:
        raise ValueError("tourist volume need to be a valid number")
    if (tourist_volume < 0):
        raise ValueError("Invalid tourist volume: tourist volume per year must be more than 0")
    return tourist_volume

def validate_duration(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        value = int(value)
    except:
        raise ValueError("Duration needs to be integer in minutes")
    if (value < 0):
        raise ValueError("Invalid value: duration must be more than 0")
    return value

def validate_distance(value):
    if value is None:
        raise ValueError("Cannot leave any fields blank.")
    try:
        value = float(value)
    except:
        raise ValueError("Distance needs to be integer/floating point")
    if (value < 0):
        raise ValueError("Invalid value: distance must be more than 0")
    return value

def validate_overseas_data(data):
    if (not check_json_keys(data, {"company","country","city","duration","distance","snow","tourist_volume_of_cable_car","cable_car_price","age_range","is_nature","type_of_trip","is_citizen"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    company = validate_null(data["company"])
    country = validate_null(data["country"])
    city = validate_null(data["city"])
    duration = validate_duration(data["duration"])
    distance = validate_distance(data["distance"])
    snow = validate_binary_encodings(data["snow"], name="snow")
    tourist_volume = validate_tourist_volume(data["tourist_volume"])
    cable_car_price = validate_price(data["cable_car_price"])
    age_range = validate_age_range(data["age_range"])
    is_nature = validate_binary_encodings(data["is_nature"], name="is_nature")
    type_of_trip = validate_binary_encodings(data["type_of_trip"], name="type_of_trip")
    is_citizen = validate_binary_encodings(data["is_citizen"], name="is_citizen")
    return company,country,city,duration,distance,snow,tourist_volume_of_cable_car,cable_car_price,age_range,is_nature,type_of_trip,is_citizen