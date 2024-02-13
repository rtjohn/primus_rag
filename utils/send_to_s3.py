import os
import boto3
from dotenv import load_dotenv
from config import bucket_name, directory1, directory2, directory3

# Not necessary if you have set up AWS CLI
load_dotenv()  # Load environment variables from .env
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3')

def list_files(directory):
    """List all files in the given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def upload_files(file_paths, bucket_name):
    """Upload files to the specified S3 bucket."""
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        try:
            response = s3.upload_file(file_path, bucket_name, file_name)
            print(f"Successfully uploaded {file_name} to {bucket_name}.")
        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")

# Loaded from config file
bucket_name = bucket_name

# This realy should be a loop of function call
directory1 = directory1
files_to_upload = list_files(directory1)
upload_files(files_to_upload, bucket_name)

directory2 = directory2
files_to_upload = list_files(directory2)
upload_files(files_to_upload, bucket_name)

directory3 = directory3
files_to_upload = list_files(directory3)
upload_files(files_to_upload, bucket_name)
