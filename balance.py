import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """AWS Lambda function to move new files from partitioned folders to the target folder"""
    
    # Define source and destination folder paths
    bucket_name = 'taza-datalake'
    base_folder = 'raw/balance/public/'
    target_folder = 'balance_transaction/'
    
    # Calculate the date for today and the previous day to check for new partitions (@Santosh Change the logic based on ingestion)
    today = datetime.today().strftime('%Y_%m')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y_%m')

    # List of folders to check (current and previous date partitions)
    date_folders = [
        f'balance_transaction_{today}/',
        f'balance_transaction_{yesterday}/'
    ]
    
    try:
        for folder in date_folders:
            move_files_from_folder(bucket_name, base_folder, folder, target_folder)
            
        return {
            'statusCode': 200,
            'body': 'Files copied successfully.'
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error occurred: {str(e)}"
        }

        
def move_files_from_folder(bucket_name, base_folder, source_folder, target_folder):
    """Move files from source folder to target folder without deleting originals for Athena to consider this as single table"""
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{base_folder}{source_folder}")
        
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                filename = os.path.basename(file_key)
                target_key = f"{base_folder}{target_folder}{filename}"
                
                # Check if the file already exists in the target folder
                if not file_exists(bucket_name, target_key):
                    copy_file(bucket_name, file_key, target_key)
                else:
                    print(f"File {filename} already exists in {target_folder}. Skipping...")
    
    except Exception as e:
        print(f"Error processing folder {source_folder}: {str(e)}")
        raise


def file_exists(bucket_name, key):
    """Check if a file exists in the specified S3 bucket"""
    
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
        return True
    except s3.exceptions.NoSuchKey:
        return False
    except Exception as e:
        print(f"Error checking if file exists: {str(e)}")
        raise


def copy_file(bucket_name, source_key, target_key):
    """Copy a file from source to target in the S3 bucket"""
    
    try:
        copy_source = {'Bucket': bucket_name, 'Key': source_key}
        s3.copy_object(Bucket=bucket_name, CopySource=copy_source, Key=target_key)
        print(f"File {os.path.basename(source_key)} copied to {target_key}.")
    except Exception as e:
        print(f"Error copying file {source_key}: {str(e)}")
        raise
