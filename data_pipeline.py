import os
import requests
import pandas as pd
import boto3
from sqlalchemy import create_engine

# Fetch data from an API
def fetch_api_data(url):
    response = requests.get(url)
    data = response.json()
    return data

# Load data from a CSV file
def load_csv_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Save data to AWS S3
def upload_to_s3(file_name, bucket, object_name=None):
    s3 = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    s3.upload_file(file_name, bucket, object_name)

# Clean and transform the data using Pandas
def clean_data(df):
    df.dropna(inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Save cleaned data to a cloud database (e.g., AWS RDS)
def save_to_rds(df, db_url, table_name):
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def main():
    api_url = 'https://api.example.com/data'  # Replace with actual API URL
    csv_file_path = 'path/to/your/csvfile.csv'  # Replace with actual CSV file path

    # Fetch data
    api_data = fetch_api_data(api_url)
    api_df = pd.DataFrame(api_data)
    csv_df = load_csv_data(csv_file_path)

    # Clean data
    cleaned_api_df = clean_data(api_df)
    cleaned_csv_df = clean_data(csv_df)

    # Save raw and cleaned data to S3
    bucket_name = 'your-bucket-name'  # Replace with your bucket name
    cleaned_api_df.to_csv('cleaned_api_data.csv', index=False)
    cleaned_csv_df.to_csv('cleaned_csv_data.csv', index=False)
    upload_to_s3('cleaned_api_data.csv', bucket_name)
    upload_to_s3('cleaned_csv_data.csv', bucket_name)

    # Save cleaned data to RDS
    db_url = 'postgresql+psycopg2://username:password@host:port/dbname'  # Replace with your RDS connection string
    save_to_rds(cleaned_api_df, db_url, 'cleaned_api_data')
    save_to_rds(cleaned_csv_df, db_url, 'cleaned_csv_data')

if __name__ == '__main__':
    main()

