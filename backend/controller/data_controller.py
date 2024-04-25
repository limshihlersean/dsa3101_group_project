from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

from model import Database
from model.MLModel import query_model
from services import price_opt_validator, noncit_single_validator, citsingle_validator, allisbundle_validator, overseas_validator, ped_validator

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

@app.route('/insert/noncitizen_single', methods=['POST'])
def insert_new_rows_noncitsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()
        for row in data: 
            company, age, events, average_price = noncit_single_validator.validate_nonccit_single_data(row)
        db.add_data_to_noncitsingle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except ValueError as ve:
        # Return the ValueError message as JSON with a status code of 400
        return jsonify({'error': str(ve)}), 400

@app.route('/insert/citizen_single', methods=['POST'])
def insert_new_rows_citsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()
        for row in data: 
            company, year, age, events, price = citsingle_validator.validate_citsingle_data(row)
        db.add_data_to_citsingle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except ValueError as ve:
        # Return the ValueError message as JSON with a status code of 400
        return jsonify({'error': str(ve)}), 400
    
@app.route("/model/priceoptmodel", methods=["POST"])
def get_optimal_price_from_ml_model():
    try:
        data = request.get_json()
        age_range, tourist_volume, is_one_way, is_citizen = price_opt_validator.validate_price_opt_data(data)
        optimal_price_based_on_ml_model = query_model.query_ml_model(age_range, tourist_volume, is_one_way, is_citizen)
        return jsonify({"optimal_price": optimal_price_based_on_ml_model})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    

@app.route('/insert/all_isbundle', methods=['POST'])
def insert_new_rows_allisbundle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()
        for row in data: 
            company, age, is_citizen, events, price, singleA, singleB, singleC, singleD, singleE = allisbundle_validator.validate_allisbundle_data(row)
        db.add_data_to_allisbundle(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except ValueError as ve:
        # Return the ValueError message as JSON with a status code of 400
        return jsonify({'error': str(ve)}), 400

@app.route('/insert/overseas', methods=['POST'])
def insert_new_rows_overseas():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()
        for row in data: 
            company, country, city, duration, distance, snow, tourist_volume, cable_car_price, age_range, is_nature, type_of_trip, is_citizen = overseas_validator.validate_overseas_data(row)

        db.add_data_to_overseas(data)
        message = "Insertion success"
        return jsonify({'message': message})
    except ValueError as ve:
        # Return the ValueError message as JSON with a status code of 400
        return jsonify({'error': str(ve)}), 400

@app.route('/insert/ped_data', methods=['POST'])
def insert_new_rows_ped():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()
        for row in data: 
            is_citizen,is_adult,price,quantity= ped_validator.validate_ped_data(row)

        db.add_data_to_ped(data)
        message = "Insertion success"
        return jsonify({'message': message})

    except ValueError as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/delete/noncitizen_single', methods=['DELETE'])
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

@app.route('/delete/citizen_single', methods=['DELETE'])
def delete_rows_citsingle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.delete_data_from_citsingle(data)
        message = "Deletion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400


@app.route('/delete/all_isbundle', methods=['DELETE'])
def delete_rows_allisbundle():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.delete_data_from_allisbundle(data)
        message = "Deletion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/delete/overseas', methods=['DELETE'])
def delete_rows_overseas():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.delete_data_from_overseas(data)
        message = "Deletion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400

@app.route('/delete/ped_data', methods=['DELETE'])
def delete_rows_ped():
    try:
        # Iterate over the JSON data and insert each row into the database
        data = request.get_json()

        db.delete_data_from_ped(data)
        message = "Deletion success"
        return jsonify({'message': message})

    except Exception as e:
        # Return an error message if there's an exception
        return jsonify({'error': str(e)}), 400