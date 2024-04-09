from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

from ..model.Database import Database

app = Flask(__name__)

db = Database()

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
