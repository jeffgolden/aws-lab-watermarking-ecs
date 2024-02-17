# Serverless Watermarking

[Blog Article](https://jeffgolden.me/posts/aws-watermarking-learning-project/)

## Services Used

- S3
- SNS
- SQS
- ECS - *Not Demonstrated in the code*
- Parameter Store
- IAM - *Not Demonstrated in the code*

## Description

This self-guided lab creates a service where, when a PNG file is uploaded to an S3 bucket it will be watermarked with the filename of the file. Then the processed Image will be deposited into the output folder of the bucket.

The purpose of this lab is to provide me with practical experience implementing a solution using the services listed above.

## Limitations

- Currently, files uploaded with a plus (+) symbol in the filename fail to process.
- Works only with PNG files now (or at least formats that PIL can understand and have an alpha layer)

