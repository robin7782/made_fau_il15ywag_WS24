import sqlite3
import pandas as pd
import os

# Define paths
data_path = "./data"
housing_file = os.path.join(data_path, "American_Housing_Data_20231209.csv")
income_file = os.path.join(data_path, "postcode_level_averages.csv")
database_file = os.path.join(data_path, "maindatabase.db")

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Process and create table for American Housing Data
housing_data = pd.read_csv(housing_file)

# Rename columns
housing_data.rename(columns={
    "Zip Code": "zip_code",
    "State": "state",
    "County": "country",
    "Living Space": "living_space",
    "Beds": "beds",
    "Baths": "baths",
    "Price": "price",
    "Median Household Income": "income"
}, inplace=True)

# Drop rows with empty cells
housing_data.dropna(inplace=True)

# Define table schema and create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hause_expense_usa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zip_code TEXT,
    state TEXT,
    country TEXT,
    living_space REAL,
    beds INTEGER,
    baths INTEGER,
    price REAL,
    income REAL
)
""")

# Insert data into the table
housing_data.to_sql("hause_expense_usa", conn, if_exists="replace", index=False)

# Process and create table for Postcode Level Averages
income_data = pd.read_csv(income_file)

# Rename columns
income_data.rename(columns={
    "zipcode": "zip_code",
    "state": "state",
    "country": "country",
    "total_income": "income"
}, inplace=True)

# Drop rows with empty cells
income_data.dropna(inplace=True)

# Define table schema and create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS income_usa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zip_code TEXT,
    state TEXT,
    country TEXT,
    income REAL
)
""")

# Insert data into the table
income_data.to_sql("income_usa", conn, if_exists="replace", index=False)

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database created successfully at: {database_file}")
