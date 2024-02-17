# Serverless Watermarking

## Services Used - *In Progress*

- S3
- SNS
- SQS
- ECS - *Not Demonstrated in the code*
- Parameter Store
- IAM - *Not Demonstrated in the code*

## Description

This experiment creates a service where, when a PNG file is uploaded to an S3 bucket it will be watermarked with the filename of the file. Then the processed Image will be deposited into the output folder of the bucket.

The purpose of this experiment is to provide me with practical experience implementing a solution in S3 using the services listed above.

## Limitations

Currently, files uploaded with a plus (+) symbol in the filename fail to process.
