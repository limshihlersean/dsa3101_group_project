def validate_age_range(age_range):
    try:
        age_range = int(age_range)
    except:
        raise ValueError("age range need to be 0, 1, 2 or 3")
    if (age_range > 3 or age_range < 0):
        raise ValueError("Invalid age range: age range need to be 0, 1, 2 or 3")
    return age_range

def validate_tourist_volume(tourist_volume):
    try:
        tourist_volume = float(tourist_volume)
    except:
        raise ValueError("tourist volume need to be a valid number")
    if (tourist_volume < 0):
        raise ValueError("Invalid tourist volume: tourist volume per year must be more than 0")
    return tourist_volume

def validate_binary_encodings(num):
    try:
        num = int(num)
    except:
        raise ValueError("num needs to be 0 and 1")
    if (num != 0 and num != 1):
        raise ValueError("Values have to be either 0 or 1")
    return num