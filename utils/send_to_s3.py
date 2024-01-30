import os
import boto3

# Ensure your AWS credentials are set in your environment, or configure boto3 to use them directly
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

bucket_name = 'dndragsystem'

directory = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/phb5e_refined'
files_to_upload = list_files(directory)
upload_files(files_to_upload, bucket_name)

directory = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/forgottenrealms_cleaned'
files_to_upload = list_files(directory)
upload_files(files_to_upload, bucket_name)

directory = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/dnd-5e_cleaned'
files_to_upload = list_files(directory)
upload_files(files_to_upload, bucket_name)
