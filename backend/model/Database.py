import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv("../.env")
mysql_password = os.environ.get("MYSQL_PASSWORD")

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="host.docker.internal",
            user="root",
            password=mysql_password,
            database="priceopt",
            port=1272
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        column_headers = [col[0] for col in self.cursor.description]
        return column_headers, self.cursor.fetchall()

    def execute_query2(self, query):
        self.cursor.execute(query)



    def retrieve_data_from_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        column_headers, table_data = self.execute_query(query)
        return column_headers, table_data



    def get_dynamic_pricing_table(self):

        query = f"SELECT * FROM citizen_single"
        column_headers, table_data = self.execute_query(query)

        return column_headers, table_data

    def get_pricing_table(self):

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
        column_headers, table_data = self.execute_query(query)

        return column_headers, table_data

    def get_local_discount_table(self):

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
        column_headers, rows = self.execute_query(query)

        return column_headers, rows


    def get_bundle_discount_table(self):

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
        column_headers, rows = self.execute_query(query)
        return column_headers, rows


    def get_distance_duration_price_table(self):
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
        rows = self.execute_query(query)

        return rows
    
    def add_all_data_to_table(self, table_name, data):
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['%s'] * len(data[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Extract values from each row of data
        values = [tuple(row.values()) for row in data]

        # Insert multiple rows of data in one go
        self.cursor.executemany(query, values)
        self.conn.commit()