import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
mysql_password = os.environ.get("MYSQL_PASSWORD")

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=mysql_password,
            database="priceopt",
            port=3306
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def retrieve_data_from_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        table_data = self.execute_query(query)
        column_headers = [col[0] for col in self.cursor.description]
        return column_headers, table_data
    
    def add_all_data_to_table(self, table_name, data):
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['%s'] * len(data[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Extract values from each row of data
        values = [tuple(row.values()) for row in data]

        # Insert multiple rows of data in one go
        self.cursor.executemany(query, values)
        self.conn.commit()


