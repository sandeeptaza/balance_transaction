# S3 File Mover Lambda Function

## Overview

This AWS Lambda function is designed to move files from date-based partition folders (e.g., `balance_transaction_2024_09/`, `balance_transaction_2024_08/`) in an S3 bucket to a target folder (`balance_transaction/`) without deleting the original files. The function runs daily and moves new files from the partition folders to the common target folder.

---

## Project Structure

- `balance.py`: The main Lambda function code that moves files.
- `unit_test.py`: Unit test code for testing the file-moving functionality using the `unittest` framework and `moto` for mocking AWS services.
- `README.md`: This documentation file.

---

## Requirements

### For AWS Lambda:
- AWS account with S3 service enabled.
- IAM Role for the Lambda function with the following permissions:
  - `s3:ListBucket`
  - `s3:GetObject`
  - `s3:PutObject`
  
### For Local Development & Testing:
- Python 3.x
- `boto3` for interacting with AWS services.
- `moto` for mocking S3 in unit tests.

You can install the necessary dependencies with the following command:

```bash
pip install boto3 moto
