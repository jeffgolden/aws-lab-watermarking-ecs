import boto3

ssm = boto3.client('ssm')


QUEUE_URL = ssm.get_parameter(Name="/watermarkimage/queue_url")["Parameter"]["Value"]
OUTPUT_BUCKET = ssm.get_parameter(Name="/watermarkimage/output_bucket")["Parameter"]["Value"]
OUTPUT_PATH = ssm.get_parameter(Name="/watermarkimage/output_path")["Parameter"]["Value"]
