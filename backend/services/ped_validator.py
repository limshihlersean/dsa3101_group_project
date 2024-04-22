from services.general_validator import validate_price, validate_binary_encodings, check_json_keys

def validate_ped_data(data):
    if (not check_json_keys(data, {"is_citizen","is_adult","price","quantity"})):
        raise KeyError("Key mismatch: Check if the name of keys are correct")
    is_citizen = validate_binary_encodings(data["is_citizen"], name="is_citizen")
    is_adult = validate_binary_encodings(data["is_adult"], name="is_adult")
    average_price = validate_price(data["average_price"])
    quantity = validate_price(data["quantity"])
    return is_citizen,is_adult,price,quantity