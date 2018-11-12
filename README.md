# About Function

An Amazon SES notification handler for processing bounces, complaints and deliveries to upload to an Amazon S3 bucket.

# Requirement

- An Amazon S3 Bucket
- An Amazon SNS Topic configured with Amazon SES Notifications

# Usage

1. Create this Lambda Function with the Bucket name
2. Subscribe the lambda endpoint to the Topic
3. Allow s3:PutObject action to created IAM role for the bucket

# License

MIT License (MIT)

This software is released under the MIT License, see license.txt.
