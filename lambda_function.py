import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        print(f"Received object: {key}")

        # Only process files from input/
        if not key.startswith('input/'):
            print("File not in input/, skipping")
            continue

        filename = os.path.basename(key)

        download_path = f"/tmp/{uuid.uuid4()}-{filename}"
        upload_path = f"/tmp/resized-{filename}"

        # Download image from S3
        s3.download_file(bucket, key, download_path)

        # Resize image
        with Image.open(download_path) as image:
            image.thumbnail((300, 300))
            image.save(upload_path)

        # Upload to output/
        output_key = f"output/{filename}"
        s3.upload_file(upload_path, bucket, output_key)

        print(f"Uploaded resized image to {output_key}")
