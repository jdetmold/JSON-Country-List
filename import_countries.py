#!/usr/bin/env python3

# This script reads a JSON file containing country data and imports it into a PostgreSQL database.
# The JSON file should be in the same directory as this script and named "CountriesList.json".
# First install the psycopg2 library by running "pip install psycopg2" in your terminal.
# Update the database connection details below with your actual database connection details.
# Run the script with "python import_countries.py" in your terminal.


import json
import psycopg2

# Update these with your actual database connection details
DB_NAME = "your_database"
DB_USER = "your_user"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def main():
    # Load the JSON data from file
    with open("CountriesList.json", "r", encoding="utf-8") as file:
        countries_data = json.load(file)
    
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Optional: Create table if not already created.
        # (Remove or comment out if you already have the table set up.)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS countries (
            name VARCHAR(100),
            calling_code INT,
            iso_a2 VARCHAR(5),
            iso_a3 VARCHAR(5),
            iso_num INT
        );
        """
        cur.execute(create_table_query)
        
        # Insert each record from the JSON
        insert_query = """
            INSERT INTO countries (name, calling_code, iso_a2, iso_a3, iso_num)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for country in countries_data:
            cur.execute(
                insert_query, 
                (
                    country["name"], 
                    country["callingCode"], 
                    country["isoA2"], 
                    country["isoA3"], 
                    country["isoNum"]
                )
            )
        
        print("Countries imported successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
