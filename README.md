# Data Pipeline with Cloud and Docker

This project demonstrates how to set up a data pipeline to ingest, process, and store data from multiple sources in a cloud environment using Docker and AWS services.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Set Up AWS S3](#step-1-set-up-aws-s3)
3. [Step 2: Set Up AWS RDS](#step-2-set-up-aws-rds)
4. [Step 3: Install AWS CLI and Configure](#step-3-install-aws-cli-and-configure)
5. [Step 4: Develop and Containerize Your Application](#step-4-develop-and-containerize-your-application)
6. [Step 5: Build and Push Docker Image to Amazon ECR](#step-5-build-and-push-docker-image-to-amazon-ecr)
7. [Step 6: Deploy the Docker Container on AWS ECS](#step-6-deploy-the-docker-container-on-aws-ecs)
8. [Documentation](#documentation)

## Prerequisites

- An AWS account
- Docker installed on your local machine
- AWS CLI installed and configured on your local machine
- Basic knowledge of Python, Docker, and AWS services

## Step 1: Set Up AWS S3

1. **Create an S3 Bucket**:
    - Log in to the AWS Management Console.
    - Navigate to the S3 service.
    - Click on "Create bucket".
    - Provide a unique name for your bucket and select the region.
    - Click "Create bucket".

2. **Configure Bucket Permissions**:
    - Click on the bucket name.
    - Navigate to the "Permissions" tab.
    - Ensure your IAM user has read/write access to the bucket.

## Step 2: Set Up AWS RDS

1. **Create an RDS Instance**:
    - Navigate to the RDS service in the AWS Management Console.
    - Click "Create database".
    - Select the database engine (e.g., PostgreSQL).
    - Configure the database settings (instance type, storage, etc.).
    - Set a master username and password.
    - Click "Create database".

2. **Configure Security Group**:
    - Ensure the security group associated with your RDS instance allows inbound traffic on the database port (default is 5432 for PostgreSQL).

## Step 3: Install AWS CLI and Configure

1. **Install AWS CLI**:
    - Follow the [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) to install the AWS CLI on your local machine.

2. **Configure AWS CLI**:
    - Open a terminal or command prompt.
    - Run `aws configure` and enter your AWS Access Key ID, Secret Access Key, default region, and output format.

## Step 4: Develop and Containerize Your Application

### 4.1 Write the Data Pipeline Script

Create a Python script (`data_pipeline.py`) with the following content:

```python
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
```

### 4.2 Create a `requirements.txt` File

Create a `requirements.txt` file with the following content:

```
boto3
pandas
requests
sqlalchemy
psycopg2-binary
```

### 4.3 Create a Dockerfile

Create a Dockerfile in the root directory of your project:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run data_pipeline.py when the container launches
CMD ["python", "data_pipeline.py"]
```

## Step 5: Build and Push Docker Image to Amazon ECR

### 5.1 Create an ECR Repository

1. **Go to the AWS Management Console**:
    - Navigate to the ECR service.
    - Click "Create repository".
    - Provide a name for the repository (e.g., `data-pipeline-repo`).
    - Click "Create repository".

### 5.2 Authenticate Docker with ECR

1. **Open Your Terminal**:
    - Make sure AWS CLI is installed and configured.

2. **Authenticate Docker**:
    - Run the following command to authenticate Docker to your Amazon ECR registry (replace `aws_region` with your AWS region and `aws_account_id` with your AWS account ID):
      ```sh
      aws ecr get-login-password --region aws_region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.aws_region.amazonaws.com
      ```

### 5.3 Build and Tag the Docker Image

1. **Navigate to Your Project Directory**:
    - Make sure you are in the root directory of your project.

2. **Build the Docker Image**:
    - Run the following command to build your Docker image:
      ```sh
      docker build -t your-repository-name .
      ```

3. **Tag the Docker Image**:
    - Tag the image with your ECR repository URI:
      ```sh
      docker tag your-repository-name:latest aws_account_id.dkr.ecr.aws_region.amazonaws.com/your-repository-name:latest
      ```

### 5.4 Push the Docker Image to ECR

1. **Push the Image**:
    - Run the following command to push the Docker image to your ECR repository:
      ```sh
      docker push aws_account_id.dkr.ecr.aws_region.amazonaws.com/your-repository-name:latest
      ```

## Step 6: Deploy the Docker Container on AWS ECS

### 6.1 Create an ECS Cluster

1. **Go to the AWS Management Console**:
    - Navigate to the ECS service.
    - Click "Clusters".
    - Click "Create Cluster".
    - Choose "EC2 Linux + Networking" or "Fargate".
    - Follow the wizard to create the cluster.

### 6.2 Create a Task Definition

1. **Navigate to Task Definitions**:
    - Click "Task Definitions".
    - Click "Create new Task Definition".
    - Choose "EC2" or "Fargate".

2. **Configure Task Definition**:
    - Add a container to the task definition.
    - Provide a name for the container.
    - For the image, use the ECR image URI: `aws_account_id.dkr.ecr.aws_region.amazonaws.com/your-repository-name:latest`.
    - Specify the CPU and memory limits.
    - Add any necessary environment variables.
    - Click "Create".

### 6.3 Run the Task

1. **Navigate to Clusters**:
    - Click on your cluster name.

2. **Run New Task**:
    - Click "Tasks".
    - Click "Run new Task".
    - Select your task definition.
    - Specify the number of tasks to run.
    - Choose the launch type (EC2 or Fargate).
    - Click "Run Task".

