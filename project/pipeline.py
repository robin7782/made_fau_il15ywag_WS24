import os
import pandas as pd
import sqlite3
import requests
from zipfile import ZipFile

def download_data():
    # Dataset URLs
    dataset_urls = [
        "https://www.kaggle.com/datasets/waqi786/medical-costs?select=medical_costs.csv",
        "https://www.kaggle.com/datasets/satyajeetrai/medical-cost?select=dataset_.csv"
    ]
    
    # Download each dataset
    for i, url in enumerate(dataset_urls, 1):
        response = requests.get(url, stream=True)
        dataset_path = f"/data/medical_costs_{i}.csv"
        
        with open(dataset_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
        print(f"Downloaded dataset {i}: {dataset_path}")

def transform_data():
    # Load datasets
    df1 = pd.read_csv("/data/medical_costs_1.csv")
    df2 = pd.read_csv("/data/medical_costs_2.csv")
    
    # Data Transformation - Handle missing values
    df1.fillna(method='ffill', inplace=True)
    df2.fillna(method='ffill', inplace=True)
    
    # Convert columns to appropriate data types (example)
    df1['age'] = df1['age'].astype(int)
    df2['age'] = df2['age'].astype(int)
    
    # Additional cleaning and transformation steps as needed
    # For example, encoding categorical variables, such as smoking status
    df1['smoking'] = df1['smoking'].map({'yes': 1, 'no': 0})
    df2['smoking'] = df2['smoking'].map({'yes': 1, 'no': 0})
    
    return df1, df2

def load_data(df1, df2):
    # Connect to SQLite database
    conn = sqlite3.connect("/data/medical_costs.db")
    
    # Load DataFrames into database
    df1.to_sql("medical_costs_waqi786", conn, if_exists="replace", index=False)
    df2.to_sql("medical_costs_satyajeet", conn, if_exists="replace", index=False)
    
    # Close the connection
    conn.close()

def main():
    download_data()
    df1, df2 = transform_data()
    load_data(df1, df2)
    print("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()
