from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

from model import Database

app = Flask(__name__)

db = Database.Database()

@app.route('/api/data', methods=['GET'])
def get_data():
    # To add model logic to get data from database and transform data.
    #data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    file_path = '../data/bundled_discount.csv'
    data = pd.read_csv(file_path)

    df = pd.DataFrame(data)
    df_json = df.to_json(orient="records")
    return jsonify(df_json)


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