import mysql.connector
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Get the directory of the current script file
#script_directory = os.path.dirname(__file__)

# Change the current working directory to the script directory
#os.chdir(script_directory)

load_dotenv()
mysql_password = os.environ.get("MYSQL_PASSWORD")

df1 = pd.read_csv('local_attractions_citizen_alacarte_allyears.csv')
df2 = pd.read_csv('local_attractions_noncitizen_alacarte_2024.csv')
df3 = pd.read_csv('local_attractions_citandnon_isbundle_2024.csv')
df4 = pd.read_csv('cable_car_cleaned_v2.csv')

while True:
    try:
        mydb = mysql.connector.connect(
            host="db", #"localhost", #change to localhost if run locally if not db when docker-compose up
            user="root",
            password=mysql_password,
            database="priceopt",
            port=3306
        )
        print("Connected to MySQL server successfully!!!")
        break  
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        print("Retrying in 5 seconds...")
        time.sleep(5)  

cursor = mydb.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS priceopt")

cursor.execute("DROP TABLE IF EXISTS local")


#######creating df1#############
cursor.execute("USE priceopt")

cursor.execute("DROP TABLE IF EXISTS citizen_single")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS citizen_single (
        company VARCHAR(255), 
        year INT,       
        age VARCHAR(50), 
        events VARCHAR(255),
        price FLOAT
    )
""")



# Iterate over DataFrame rows and insert data into MySQL table
for index, row in df1.iterrows():
    sql = "INSERT INTO citizen_single (company, year, age, events, price) VALUES (%s, %s, %s, %s, %s)"
    val = (row['company'], row['year'], row['age'], row['events'], row['average_price'])
    cursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

cursor.execute("SELECT COUNT(*) FROM citizen_single")

# Fetch the result of the query
num_rows = cursor.fetchone()[0]

# Print the number of rows
print("Number of rows in 'citizen_single' table:", num_rows)


#######creating df2#############
cursor.execute("USE priceopt")

cursor.execute("DROP TABLE IF EXISTS noncitizen_single")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS noncitizen_single (
        company VARCHAR(255),      
        age VARCHAR(50), 
        events VARCHAR(255),
        price FLOAT
    )
""")



# Iterate over DataFrame rows and insert data into MySQL table
for index, row in df2.iterrows():
    sql = "INSERT INTO noncitizen_single (company, age, events, price) VALUES (%s, %s, %s, %s)"
    val = (row['company'], row['age'], row['events'], row['average_price'])
    cursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

cursor.execute("SELECT COUNT(*) FROM noncitizen_single")

# Fetch the result of the query
num_rows = cursor.fetchone()[0]

# Print the number of rows
print("Number of rows in 'noncitizen_single' table:", num_rows)


#######creating df3#############
cursor.execute("USE priceopt")

cursor.execute("DROP TABLE IF EXISTS all_isbundle")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS all_isbundle (
        company VARCHAR(255),       
        age VARCHAR(50), 
        is_citizen INT,
        events VARCHAR(255),
        price INT
    )
""")



# Iterate over DataFrame rows and insert data into MySQL table
for index, row in df3.iterrows():
    sql = "INSERT INTO all_isbundle (company, age, is_citizen, events, price) VALUES (%s, %s, %s, %s, %s)"
    val = (row['company'], row['age'], row['is_citizen'], row['events'], row['average_price'])
    cursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

cursor.execute("SELECT COUNT(*) FROM all_isbundle")

# Fetch the result of the query
num_rows = cursor.fetchone()[0]

# Print the number of rows
print("Number of rows in 'all_isbundle' table:", num_rows)



#######creating df4#############
cursor.execute("USE priceopt")

cursor.execute("DROP TABLE IF EXISTS overseas")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS overseas (
        company VARCHAR(255),
        country VARCHAR(255),
        city VARCHAR(255),
        duration INT,
        distance FLOAT,
        snow INT,
        tourist_volume_of_cable_car INT,
        cable_car_price DECIMAL(10, 2),
        age_range INT,
        is_nature INT,
        type_of_trip INT,
        is_citizen INT
    )
""")

for index, row in df4.iterrows():
    sql = "INSERT INTO overseas (company, country, city, duration, distance, snow, tourist_volume_of_cable_car, cable_car_price, age_range, is_nature, type_of_trip, is_citizen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (row['company'], row['country'], row['city'], row['duration'], row['distance'], row['snow'], row['tourist_volume_of_cable_car'], row['cable_car_price'], row['age_range'], row['is_nature'], row['type_of_trip'], row['is_citizen'])
    cursor.execute(sql, val)
# Commit changes to the database
mydb.commit()


cursor.execute("SELECT COUNT(*) FROM overseas")

# Fetch the result of the query
num_rows = cursor.fetchone()[0]

# Print the number of rows
print("Number of rows in 'overseas' table:", num_rows)


# Close cursor and connection
cursor.close()
mydb.close()