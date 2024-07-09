# data_ingestion.py

import requests
import boto3
import pandas as pd
import json
from io import StringIO

def fetch_api_data():
    response = requests.get('https://api.example.com/data')
    data = response.json()
    return data

def upload_to_s3(data, bucket_name, file_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))

def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def upload_csv_to_s3(df, bucket_name, file_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())

if __name__ == "__main__":
    # Fetch and upload API data
    data = fetch_api_data()
    upload_to_s3(data, 'your-bucket-name', 'data/raw/api_data.json')

    # Read and upload CSV data
    df = read_csv_file('local_path_to_csv.csv')
    upload_csv_to_s3(df, 'your-bucket-name', 'data/raw/csv_data.csv')
