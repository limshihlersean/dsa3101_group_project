from services.general_validator import validate_age_string, validate_price, validate_null, check_json_keys

def validate_nonccit_single_data(data):
    if (not check_json_keys(data, {"company", "age", "events", "price"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    company = validate_null(data["company"])
    age = validate_age_string(data["age"])
    events = validate_null(data["events"])
    price = validate_price(data["price"])
    return company, age, events, price