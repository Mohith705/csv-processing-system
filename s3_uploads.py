import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY_ID = 'AKIAQPJZEXEN3P6C2Y7W'
SECRET_ACCESS_KEY = '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'

def upload_file_from_device(file_path, bucket, file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(file_data, bucket, file_name)
        print("Upload Successful")
        
        file_url = f"https://{bucket}.s3.amazonaws.com/{file_name}"
        return file_url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
