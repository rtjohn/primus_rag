def read_file_from_s3(bucket_name, file_key):
    """
    Reads a file from an AWS S3 bucket and returns its content as a string.

    This function initializes a connection to an S3 resource using boto3, 
    retrieves the specified object from the given bucket, and then reads 
    the content of the file. The content is decoded from bytes to a UTF-8 
    string before being returned.

    Parameters:
    bucket_name (str): The name of the S3 bucket.
    file_key (str): The key (path) of the file within the S3 bucket.

    Returns:
    str: The content of the file as a decoded string.
    """
    s3 = boto3.resource('s3')

    # Get the object from the bucket
    obj = s3.Object(bucket_name, file_key)

    # Read the file's content
    file_content = obj.get()['Body'].read().decode('utf-8')
    
    return file_content


# Reading in the 5th edition PHB from S3
bucket_name = 'dndragsystem'
file_key = 'phb5e.txt'
file_content = read_file_from_s3(bucket_name, file_key)