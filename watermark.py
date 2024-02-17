from PIL import Image, ImageDraw, ImageFont
from parameters import QUEUE_URL, OUTPUT_BUCKET, OUTPUT_PATH
from urllib.parse import unquote_plus
import boto3
import io
import json
import logging
import posixpath


logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')
logger : logging.Logger = logging.getLogger()



def split_s3_key(key : str) -> tuple[str:str]:
    """
    Splits the S3 key into path and filename.

    Parameters:
    key (str): The S3 key.

    Returns:
    tuple[str, str]: A tuple containing the path and filename.
    """
    path, filename = posixpath.split(key)
    return path, filename

def poll_sqs_messages():
    """
    Polls messages from an SQS queue.

    This function continuously polls messages from an SQS queue and processes them.
    """
    sqs = boto3.client('sqs')
   
    while True:
        # Receive messae from SQS queue
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            AttributeNames = ['All'],
            MaxNumberOfMessages = 1,
            WaitTimeSeconds = 20
        )
        
        messages = response.get('Messages', [])
        if messages:
            for message in messages:
                logger.info(f"Processing message: {message['MessageId']}")
                message_body = json.loads(message['Body'])
                for record in message_body['Records']:
                    bucket_name = record['s3']['bucket']['name']
                    object_key = unquote_plus(record['s3']['object']['key']) # Assumes there are no plus characters in uploads
                    _, filename = split_s3_key(object_key)
                    output_key = f"{OUTPUT_PATH}/{filename}"
                    try:
                        add_watermark(bucket_name, object_key, output_key, filename)
                    except Exception as ex:
                        logger.error("Watermarking process failed for %s", object_key, exc_info=True)
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
        else:
            logger.info("No messages to process")
        

def textsize(text : str, font: ImageFont)  -> tuple[float,float]:
    """
    Calculate the size of the text to be drawn, in pixels.

    Parameters:
    text (str): The text to be drawn.
    font (ImageFont): The font to be used.

    Returns:
    tuple[float, float]: The width and height of the text.
    """
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_watermark(input_bucket : str, 
                  input_key: str, 
                  output_key: str, 
                  watermark_text: str) -> None:
    """
    Add a watermark to an image and upload it to S3.

    Parameters:
    input_bucket (str): The name of the S3 bucket where the original image is stored.
    input_key (str): The key of the original image in the S3 bucket.
    output_key (str): The key to use when uploading the watermarked image to S3.
    watermark_text (str): The text to use as a watermark.

    Returns:
    None
    """
    
    try:
        # Download the image from S3    
        s3 = boto3.client('s3')
        file_byte_string = s3.get_object(
            Bucket=input_bucket,
            Key=input_key,
        )['Body'].read()
        original_image = Image.open(io.BytesIO(file_byte_string))
    except Exception as ex:
        logger.error("Error downloading object from S3 bucket=%s key=%s", input_bucket, input_key, exc_info=True)
        raise ex
    
    try:        
        # Make the image editable
        txt = Image.new('RGBA', original_image.size, (255,255,255,0))
        
        # Choose a font and size for the watermark
        # Ensure the font is accesible in your environment or Lambda Package
        font = ImageFont.truetype('./Roboto/Roboto-Regular.ttf', 36)
        draw = ImageDraw.Draw(txt)
        textwidth, textheight = textsize(watermark_text, font)
        
        width, height = original_image.size
        x = width - textwidth
        y = height - textheight
        
        draw.text((x,y), watermark_text, fill=(0,0,0, 128), font=font)
        watermarked = Image.alpha_composite(original_image.convert('RGBA'), txt)
        
        in_mem_file=io.BytesIO()
        watermarked.save(in_mem_file, format=original_image.format)
        in_mem_file.seek(0)
    except Exception as ex:
        logger.error("Error watermarking image", exc_info=True)
        raise ex
    
    try:
        s3.upload_fileobj(in_mem_file, OUTPUT_BUCKET, output_key)
        logger.info("Successfully watermarked and uploaded %s/%s  to %s/%s", input_bucket,input_key,OUTPUT_BUCKET,output_key)
    except Exception as ex:
        logger.error("Error uploading watermarked image bucket=%s key=%s", OUTPUT_BUCKET, output_key, exc_info=True)
        raise ex
        
if __name__ == "__main__":
    """
    Main entry point of the script. It starts by polling messages from the SQS queue.
    """
    poll_sqs_messages()