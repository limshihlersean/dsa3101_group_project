from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

from model import Database
from model.MLModel import query_model
from services import data_validation

app = Flask(__name__)

db = Database.Database()


@app.route('/tables/<table_name>', methods=['GET'])
def retrieve_table_api(table_name):
    # Call the retrieve_data function to fetch data for the specified table
    table_data = db.retrieve_data_from_table(table_name)
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/tables/dynamic_pricing', methods=['GET'])
def dynamic_pricing_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = db.get_dynamic_pricing_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/tables/pricing', methods=['GET'])
def pricing_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = db.get_pricing_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/tables/local_discount', methods=['GET'])
def local_discount_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = db.get_local_discount_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/tables/bundle_discount', methods=['GET'])
def bundle_discount_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = db.get_bundle_discount_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/tables/distance_duration_price', methods=['GET'])
def distance_duration_price_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = db.get_distance_duration_price_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

@app.route('/insert/noncitsingle', methods=['POST'])
def insert_new_rows_noncitsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.add_data_to_noncitsingle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/insert/citsingle', methods=['POST'])
def insert_new_rows_citsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.add_data_to_citsingle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400
    
@app.route("/model/priceoptmodel", methods=["POST"])
def get_optimal_price_from_ml_model():
    try:
        data = request.get_json()
        age_range = data_validation.validate_age_range(data["age_range"])
        tourist_volume = data_validation.validate_tourist_volume(data["tourist_volume"])
        is_one_way = data_validation.validate_binary_encodings(data["is_one_way"])
        is_citizen = data_validation.validate_binary_encodings(data["is_citizen"])
        optimal_price_based_on_ml_model = query_model.query_ml_model(age_range, tourist_volume, is_one_way, is_citizen)
        return jsonify({"optimal_price": optimal_price_based_on_ml_model})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    

@app.route('/insert/allisbundle', methods=['POST'])
def insert_new_rows_allisbundle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.add_data_to_allisbundle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/insert/overseas', methods=['POST'])
def insert_new_rows_overseas():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.add_data_to_overseas(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/insert/ped', methods=['POST'])
def insert_new_rows_ped():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.add_data_to_ped(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/delete/noncitsingle', methods=['DELETE'])
def delete_rows_noncitsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.delete_data_from_noncitsingle(data)
        message = "Deletion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400