import json
import urllib.parse
import boto3 
import io
from PIL import Image

s3 = boto3.client('s3')

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        # Extract the file key (decode URL encoding)
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        
        print(f"Triggered by file upload: {key}")
        
        # --- SAFEGUARD 1: PREVENT INFINITE LOOPS ---
        # If the file is already in the thumbnails/ folder, do not process it again!
        if key.startswith('thumbnails/'):
            print(f"Skipping already processed thumbnail: {key}")
            continue
            
        # --- SAFEGUARD 2: FILTER NON-IMAGES ---
        # Only process actual image files. Ignore pdf, txt, zip, video, etc.
        valid_extensions = ('.jpg', '.jpeg', '.png')
        if not key.lower().endswith(valid_extensions):
            print(f"Skipping non-image file: {key}")
            continue
            
        try:
            print(f"Downloading {key} from {bucket}...")
            response = s3.get_object(Bucket=bucket, Key=key)
            image_content = response['Body'].read()
            
            # --- PROCESS THE IMAGE ---
            print("Resizing image...")
            with Image.open(io.BytesIO(image_content)) as img:
                # Resize keeping aspect ratio, max size 200x200
                img.thumbnail((200, 200))
                
                # Save to a temporary memory buffer
                buffer = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(buffer, img_format)
                buffer.seek(0)
            
            # --- UPLOAD THE THUMBNAIL ---
            # Prefix the new file with 'thumbnails/'
            new_key = f"thumbnails/{key}"
            
            print(f"Uploading thumbnail to: {new_key}")
            s3.put_object(
                Bucket=bucket,
                Key=new_key,
                Body=buffer,
                ContentType=response.get('ContentType', 'image/jpeg')
            )
            
            print("Thumbnail generation complete!")
            
        except Exception as e:
            print(f"Error processing object {key} from bucket {bucket}: {str(e)}")
            raise e
            
    return {"statusCode": 200, "body": json.dumps("Successfully processed records.")}
