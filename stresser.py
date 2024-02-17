import boto3
import uuid
from parameters import OUTPUT_BUCKET

# This is just a sample script to stress test the watermarking application
# It will upload the same file to S3 multiple times
# This is useful to test the application's ability to handle multiple requests and automatically scale
# You need to have a profile with permissions to upload files to the S3 bucket as the default profile or
# you can set the AWS_PROFILE environment variable to the name of the profile you want to use

def upload_file_to_s3(file_name, bucket_name, prefix):
    
    # Initialize a boto3 client
    s3 = boto3.client('s3')
    
    loop_count = 0
    while True:
        loop_count +=1
        # Generate a unique file name
        unique_file_name = f"{uuid.uuid4()}.png"
        # Create the full key for the S3 object
        s3_key = f"{prefix}/{unique_file_name}"

        try:
            # Upload the file to S3
            s3.upload_file(file_name, bucket_name, s3_key)
            print(f"File uploaded successfully to {bucket_name}/{s3_key}  (loop count: {loop_count})")
        except Exception as e:
            print(f"Error uploading file: {str(e)} (loop count: {loop_count})")
            
# Example usage
if __name__ == "__main__":
    
    file_name = "image.png"  # Assume the file is in the current directory
    bucket_name = OUTPUT_BUCKET # This should be the same as the input bucket so using it here to avoid hardcoing it.
    prefix = "input" # Change this if you changed your input bucket prefix
    upload_file_to_s3(file_name, bucket_name, prefix)
