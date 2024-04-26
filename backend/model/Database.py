import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv("../.env")
mysql_password = os.environ.get("MYSQL_PASSWORD")

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="db",
            user="root",
            password=mysql_password,
            database="priceopt"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        column_headers = [col[0] for col in self.cursor.description]
        return column_headers, self.cursor.fetchall()

    def execute_query_post(self, query,values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def execute_query_select(self, query, values):
        try:
            # Execute the SELECT query with the provided values
            self.cursor.execute(query, values)
            # Fetch the result of the query
            result = self.cursor.fetchall()
            # Check if the result is not None (i.e., the row exists)
            if result is not None:
                return True  # Return True if the row exists
            else:
                return False  # Return False if the row does not exist
        except Exception as e:
            # Print or log the error message if an exception occurs
            print(f"Error executing SELECT query: {e}")
            return False  # Return False in case of an error



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
                is_citizen,
                price,
                original_price,
                ((original_price - price) / original_price) * 100 AS discount
            FROM (
                SELECT 
                    company,
                    age,
                    is_citizen,
                    price,
                    (singleA + singleB + singleC + singleD + singleE) AS original_price
                FROM 
                    all_isbundle
            ) AS subquery_alias;


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

    def add_data_to_noncitsingle(self, data):
        for row in data:
            company = row.get("company")
            age = row.get("age")
            events = row.get("events")
            price = row.get("price")

            # Check if the record already exists
            query = "SELECT * FROM noncitizen_single WHERE company = %s AND age = %s AND events = %s AND price = %s"
            self.cursor.execute(query, (company, age, events, price))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Record already exists, decide whether to update or ignore
                # For example, you can update the existing record here
                # Update query: 
                # update_query = "UPDATE noncitizen_single SET ... WHERE <condition>"
                # self.cursor.execute(update_query, (new_values))
                # self.conn.commit()
                pass
            else:
                # Record does not exist, insert new record
                insert_query = "INSERT INTO noncitizen_single (`company`, `age`, `events`, `price`) VALUES (%s, %s, %s, %s);"
                values = (company, age, events, price)
                self.execute_query_post(insert_query, values)

    def add_data_to_citsingle(self, data):
        for row in data:
            company = row.get("company")
            year = row.get("year")
            age = row.get("age")
            events = row.get("events")
            price = row.get("price")

            # Check if the record already exists
            query = "SELECT * FROM citizen_single WHERE company = %s AND year = %s AND age = %s AND events = %s AND price = %s"
            self.cursor.execute(query, (company, year, age, events, price))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Record already exists, decide whether to update or ignore
                # For example, you can update the existing record here
                # Update query: 
                # update_query = "UPDATE citizen_single SET ... WHERE <condition>"
                # self.cursor.execute(update_query, (new_values))
                # self.conn.commit()
                pass
            else:
                # Record does not exist, insert new record
                insert_query = "INSERT INTO citizen_single (`company`, `year`, `age`, `events`, `price`) VALUES (%s, %s, %s, %s, %s);"
                values = (company, year, age, events, price)
                self.execute_query_post(insert_query, values)
    
    def add_data_to_allisbundle(self, data):
        for row in data:
            company = row.get("company")
            age = row.get("age")
            is_citizen = row.get("is_citizen")
            events = row.get("events")
            price = row.get("price")
            singleA = row.get("singleA")
            singleB = row.get("singleB")
            singleC = row.get("singleC")
            singleD = row.get("singleD")
            singleE = row.get("singleE")

            # Check if the record already exists
            query = "SELECT * FROM all_isbundle WHERE company = %s AND age = %s AND is_citizen = %s AND events = %s AND price = %s AND singleA = %s AND singleB = %s AND singleC = %s AND singleD = %s AND singleE = %s"
            self.cursor.execute(query, (company, age, is_citizen, events, price, singleA, singleB, singleC, singleD, singleE))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Record already exists, decide whether to update or ignore
                # For example, you can update the existing record here
                # Update query: 
                # update_query = "UPDATE all_isbundle SET ... WHERE <condition>"
                # self.cursor.execute(update_query, (new_values))
                # self.conn.commit()
                pass
            else:
                # Record does not exist, insert new record
                insert_query = "INSERT INTO all_isbundle (`company`, `age`, `is_citizen`, `events`, `price`, `singleA`, `singleB`, `singleC`, `singleD`, `singleE`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                values = (company, age, is_citizen, events, price, singleA, singleB, singleC, singleD, singleE)
                self.execute_query_post(insert_query, values)

    def add_data_to_overseas(self, data):
        for row in data:
            company = row.get("company")
            country = row.get("country")
            city = row.get("city")
            duration = row.get("duration")
            distance = row.get("distance")
            snow = row.get("snow")
            tourist_volume_of_cable_car = row.get("tourist_volume_of_cable_car")
            cable_car_price = row.get("cable_car_price")
            age_range = row.get("age_range")
            is_nature = row.get("is_nature")
            type_of_trip = row.get("type_of_trip")
            is_citizen = row.get("is_citizen")

            # Check if the record already exists
            query = "SELECT * FROM overseas WHERE company = %s AND country = %s AND city = %s AND duration = %s AND distance = %s AND snow = %s AND tourist_volume_of_cable_car = %s AND cable_car_price = %s AND age_range = %s AND is_nature = %s AND type_of_trip = %s AND is_citizen = %s"
            self.cursor.execute(query, (company, country, city, duration, distance, snow, tourist_volume_of_cable_car, cable_car_price, age_range, is_nature, type_of_trip, is_citizen))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Record already exists, decide whether to update or ignore
                # For example, you can update the existing record here
                # Update query: 
                # update_query = "UPDATE overseas SET ... WHERE <condition>"
                # self.cursor.execute(update_query, (new_values))
                # self.conn.commit()
                pass
            else:
                # Record does not exist, insert new record
                insert_query = "INSERT INTO overseas (`company`, `country`, `city`, `duration`, `distance`, `snow`, `tourist_volume_of_cable_car`, `cable_car_price`, `age_range`, `is_nature`, `type_of_trip`, `is_citizen`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                values = (company, country, city, duration, distance, snow, tourist_volume_of_cable_car, cable_car_price, age_range, is_nature, type_of_trip, is_citizen)
                self.execute_query_post(insert_query, values)

    # Inserting Data into PED 
    def add_data_to_ped(self, data):
        for row in data:
            is_citizen = row.get("is_citizen")
            is_adult = row.get("is_adult")
            price = row.get("price")
            quantity = row.get("quantity")

            # Check if the record already exists
            query = "SELECT * FROM ped_data WHERE is_citizen = %s AND is_adult = %s AND price = %s AND quantity = %s"
            self.cursor.execute(query, (is_citizen, is_adult, price, quantity))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Record already exists, decide whether to update or ignore
                # For example, you can update the existing record here
                # Update query: 
                # update_query = "UPDATE ped_data SET ... WHERE <condition>"
                # self.cursor.execute(update_query, (new_values))
                # self.conn.commit()
                pass
            else:
                # Record does not exist, insert new record
                insert_query = "INSERT INTO ped_data (`is_citizen`, `is_adult`, `price`, `quantity`) VALUES (%s, %s, %s, %s);"
                values = (is_citizen, is_adult, price, quantity)
                self.execute_query_post(insert_query, values)

    def delete_data_from_noncitsingle(self, data):
        for _, row in data.items():
            query_select = "SELECT * FROM noncitizen_single WHERE company=%s AND age=%s AND events=%s AND price=%s;"
            company = row.get("company")
            age = row.get("age")
            events = row.get("events")
            price = row.get("price")
            values = (company, age, events, price)
            # Check if the row exists in the database
            if self.execute_query_select(query_select, values):
                # If the row exists, then proceed with deletion
                query_delete = "DELETE FROM noncitizen_single WHERE company=%s AND age=%s AND events=%s AND price=%s;"
                self.execute_query_post(query_delete, values)
            else:
                # If the row doesn't exist, log a message or raise an exception as per your requirement
                print("Row not found in database:", values)

    def delete_data_from_citsingle(self,data):
        for _, row in data.items():
            # query_select = "SELECT * FROM citizen_single WHERE company=%s AND year=%s AND age=%s AND events=%s AND price=%s;"
            query_select = "SELECT * FROM citizen_single WHERE company=%s AND year=%s AND age=%s;"
            company = row.get("company")
            year = row.get("year")
            age = row.get("age")
            # events = row.get("events")
            # price = row.get("price")
            values = (company,year,age)
            # values = (company,year,age,events,price)
            if self.execute_query_select(query_select, values):
                # query_delete = "DELETE FROM citizen_single WHERE company=%s AND year=%s AND age=%s AND events=%s AND price=%s;"
                query_delete = "DELETE FROM citizen_single WHERE company=%s AND year=%s AND age=%s;"
                self.execute_query_post(query_delete,values)
            else:
                # If the row doesn't exist, log a message or raise an exception as per your requirement
                print("Row not found in database:", values)

    def delete_data_from_allisbundle(self,data):
        for _, row in data.items():
            # query_select = "SELECT * FROM all_isbundle WHERE company=%s AND age=%s AND is_citizen=%s AND events=%s AND price=%s AND singleA=%s AND singleB=%s AND singleC=%s AND singleD=%s AND singleE=%s;"
            query_select = "SELECT * FROM all_isbundle WHERE company=%s AND age=%s AND is_citizen=%s;"
            company = row.get("company")
            age = row.get("age")
            is_citizen = row.get("is_citizen")
            # events = row.get("events")
            # price = row.get("price")
            # singleA = row.get("singleA")
            # singleB = row.get("singleB")
            # singleC = row.get("singleC")
            # singleD = row.get("singleD")
            # singleE = row.get("singleE")
            # values = (company,age,is_citizen,events,price,singleA,singleB,singleC,singleD,singleE)
            values = (company,age,is_citizen)
            if self.execute_query_select(query_select, values):
                # query_delete = "DELETE FROM all_isbundle WHERE company=%s AND age=%s AND is_citizen=%s AND events=%s AND price=%s AND singleA=%s AND singleB=%s AND singleC=%s AND singleD=%s AND singleE=%s;"
                query_delete = "DELETE FROM all_isbundle WHERE company=%s AND age=%s AND is_citizen=%s;"
                self.execute_query_post(query_delete,values)
            else:
                # If the row doesn't exist, log a message or raise an exception as per your requirement
                print("Row not found in database:", values)

    def delete_data_from_overseas(self,data):
        for _, row in data.items():
            # query_select = "SELECT * FROM overseas WHERE company=%s AND country=%s AND city=%s AND duration=%s AND distance=%s AND snow=%s AND tourist_volume_of_cable_car=%s AND cable_car_price=%s AND age_range=%s AND is_nature=%s AND type_of_trip=%s AND is_citizen=%s;"
            # company = row.get("company")
            # country = row.get("country")
            # city = row.get("city")
            # duration = row.get("duration")
            # distance = row.get("distance")
            # snow = row.get("snow")
            # tourist_volume_of_cable_car = row.get("tourist_volume_of_cable_car")
            # cable_car_price = row.get("cable_car_price")
            # age_range = row.get("age_range")
            # is_nature = row.get("is_nature")
            # type_of_trip = row.get("type_of_trip")
            # is_citizen = row.get("is_citizen")
            query_select = "SELECT * FROM overseas WHERE company=%s AND age_range=%s AND type_of_trip=%s AND is_citizen=%s;"
            company = row.get("company")
            age_range = row.get("age_range")
            type_of_trip = row.get("type_of_trip")
            is_citizen = row.get("is_citizen")


            values = (company,age_range,type_of_trip,is_citizen)
            if self.execute_query_select(query_select, values):
                query_delete = "DELETE FROM overseas WHERE company=%s AND age_range=%s AND type_of_trip=%s AND is_citizen=%s;"
                self.execute_query_post(query_delete,values)
            else:
                # If the row doesn't exist, log a message or raise an exception as per your requirement
                print("Row not found in database:", values)

    def delete_data_from_ped(self,data):
        for _, row in data.items():
            query_select = "SELECT * FROM ped_data WHERE is_citizen=%s AND is_adult=%s AND price=%s AND quantity=%s;"
            is_citizen = row.get("is_citizen")
            is_adult = row.get("is_adult")
            price = row.get("price")
            quantity = row.get("quantity")

            values = (is_citizen,is_adult,price,quantity)
            if self.execute_query_select(query_select, values):
                query_delete = "DELETE FROM ped_data WHERE is_citizen=%s AND is_adult=%s AND price=%s AND quantity=%s;"
                self.execute_query_post(query_delete,values)
            else:
                # If the row doesn't exist, log a message or raise an exception as per your requirement
                print("Row not found in database:", values)


