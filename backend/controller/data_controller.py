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

def get_dynamic_pricing_table():
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = f"SELECT * FROM citizen_single"
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/dynamic_pricing', methods=['GET'])
def dynamic_pricing_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = get_dynamic_pricing_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

def get_pricing_table():
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = """
        SELECT 
            'overseas' AS table_name,
            company, 
            CASE 
                WHEN age_range = 0 THEN 'Child'
                WHEN age_range = 1 THEN 'Student'
                WHEN age_range = 2 THEN 'Adult'
                WHEN age_range = 3 THEN 'Senior Citizen'
                WHEN age_range = 4 THEN 'Disabled'
            END AS age,
            AVG(cable_car_price) AS price 
        FROM 
            overseas 
        WHERE 
            is_citizen = 1 AND 
            type_of_trip = 0 
        GROUP BY 
            company, 
            age_range

        UNION ALL

        SELECT 
            'local' AS table_name,
            company, 
            age, 
            price 
        FROM 
            citizen_single 
        WHERE 
            year = 2024;"""
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/pricing', methods=['GET'])
def pricing_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = get_pricing_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response

def get_local_discount_table():
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = """
        WITH combined_table AS (
            SELECT
                company,
                age,
                SUM(CASE WHEN is_citizen = 1 THEN price ELSE Null END) AS citizen_price,
                SUM(CASE WHEN is_citizen = 0 THEN price ELSE Null END) AS non_citizen_price
            FROM
                (
                SELECT company, age, price, 1 AS is_citizen FROM citizen_single WHERE year = 2024
                UNION ALL
                SELECT company, age, price, 0 AS is_citizen FROM noncitizen_single
                ) AS combined_table
            GROUP BY
                company,
                age
            HAVING
                citizen_price IS NOT Null OR non_citizen_price IS NOT Null
        )
        SELECT 
            company, 
            age, 
            citizen_price, 
            non_citizen_price,
            (ABS((non_citizen_price - citizen_price)) / non_citizen_price) * 100 AS discount
        FROM 
            combined_table
        WHERE 
            citizen_price != non_citizen_price;
    
    """
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/local_discount', methods=['GET'])
def local_discount_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = get_local_discount_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response




def get_bundle_discount_table():
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = """
        SELECT 
            company, 
            age, 
            price, 
            1 AS is_bundle 
        FROM all_isbundle 
        WHERE is_citizen = 1

        UNION ALL

        SELECT 
            company, 
            age, 
            price, 
            0 AS is_bundle 
        FROM citizen_single 
        WHERE year = 2024;
    
    """
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/bundle_discount', methods=['GET'])
def bundle_discount_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = get_bundle_discount_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response



def get_distance_duration_price_table():
    mydb = connect_to_database()
    cursor = mydb.cursor()

    query = """
        SELECT
            company,
            country,
            city,
            duration,
            distance,
            tourist_volume_of_cable_car AS vol,
            AVG(cable_car_price) AS price
        FROM
            overseas
        WHERE
            age_range = 2 AND is_citizen = 1
        GROUP BY
            company,
            country,
            city,
            duration,
            distance,
            vol;
    
    """
    cursor.execute(query)
    column_headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()


    cursor.close()
    mydb.close()

    return column_headers, rows

@app.route('/tables/distance_duration_price', methods=['GET'])
def distance_duration_price_table_api():
    # Call the get_pricing_table function to fetch data
    table_data = get_distance_duration_price_table()
    # Convert the data to JSON format
    response = jsonify(table_data)
    # Return the JSON response
    return response
