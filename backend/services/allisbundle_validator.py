from services.general_validator import validate_age_string, validate_price, validate_binary_encodings, validate_null, validate_year, check_json_keys

def validate_allisbundle_data(data):
    if (not check_json_keys(data, {"company","age", "is_citizen", "events", "average_price", "singleA","singleB","singleC","singleD","singleE"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    company = validate_null(data["company"])
    age = validate_age_string(data["age"])
    is_citizen = validate_binary_encodings(data["is_citizen"], name="is_citizen")
    events = validate_null(data["events"])
    average_price = validate_price(data["average_price"])
    singleA = validate_price(data["singleA"])
    singleB = validate_price(data["singleB"])
    singleC = validate_price(data["singleC"])
    singleD = validate_price(data["singleD"])
    singleE = validate_price(data["singleE"])
    return company, age, is_citizen, events, average_price, singleA, singleB, singleC, singleD, singleE