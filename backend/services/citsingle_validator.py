from services.general_validator import validate_age_string, validate_price, validate_null, validate_year, check_json_keys

def validate_citsingle_data(data):
    if (not check_json_keys(data, {"company", "year","age", "events", "price"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    company = validate_null(data["company"])
    year = validate_year(data["year"])
    age = validate_age_string(data["age"])
    events = validate_null(data["events"])
    price = validate_price(data["price"])
    return company, year, age, events, price