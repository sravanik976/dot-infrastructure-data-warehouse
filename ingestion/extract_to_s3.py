import os
import io
import boto3
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="dot_operations",
    user="dot_admin",
    password="dot_password"
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

bucket_name = os.getenv("S3_BUCKET_NAME")
tables = ["regions", "assets", "maintenance_logs"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table};", conn)
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False)

    s3_key = f"raw/{table}/{table}.parquet"
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=parquet_buffer.getvalue())
    print(f"Uploaded {table} ({len(df)} rows) to s3://{bucket_name}/{s3_key}")

conn.close()
print("All tables successfully extracted to AWS S3 Data Lake!")
