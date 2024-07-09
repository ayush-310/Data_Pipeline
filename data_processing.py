# data_processing.py

import pandas as pd
from sqlalchemy import create_engine

def clean_and_transform_data(df):
    df_cleaned = df.dropna()
    df_transformed = df_cleaned.apply(lambda x: x * 2)  # Example transformation
    return df_transformed

def store_in_rds(df, db_url, table_name):
    engine = create_engine(db_url)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

if __name__ == "__main__":
    # Load data from S3
    df = pd.read_csv('s3://your-bucket-name/data/raw/csv_data.csv')

    # Clean and transform data
    df_transformed = clean_and_transform_data(df)

    # Store processed data in RDS
    store_in_rds(df_transformed, 'postgresql://user:password@host/dbname', 'processed_data')
