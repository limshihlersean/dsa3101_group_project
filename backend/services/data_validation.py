def validate_age_range(age_range):
    if (age_range <= 3 and age_range >= 0):
        return age_range
    raise ValueError("Invalid age range: age range is between 0 and 3")

def validate_tourist_volume(tourist_volume):
    if (tourist_volume > 0):
        return tourist_volume
    raise ValueError("Invalid tourist volume: tourist volume per year must be more than 0")

def validate_binary_encodings(num):
    if (num == 0 or num == 1):
        return num
    raise ValueError("Values have to be either 0 or 1")