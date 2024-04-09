from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # To add model logic to get data from database and transform data.
    #data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    file_path = '../data/bundled_discount.csv'
    data = pd.read_csv(file_path)

    df = pd.DataFrame(data)
    df_json = df.to_json(orient="records")
    return jsonify(df_json)

def connect_to_database():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="teamVamos123!",
        database="priceopt",
        port=3306
    )
    return mydb

def retrieve_data(table_name):
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/<table_name>', methods=['GET'])
def retrieve_table_api(table_name):
    # Call the retrieve_data function to fetch data for the specified table
    table_data = retrieve_data(table_name)
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response
