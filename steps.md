# Setup and Deployment

## Step 1: Prepare the Lambda Function

1. **Copy the Lambda function code** from `lambda_function.py`.

2. **Create or use an existing S3 bucket** with the following folder structure:
   - Date-based partition folders: `balance_transaction_YYYY_MM/` (e.g., `balance_transaction_2024_09/`).
   - Target folder: `balance_transaction/` (this is where the files will be moved).

3. **Create the Lambda function in AWS**:
   - Go to the AWS Management Console.
   - Navigate to **AWS Lambda** and create a new Lambda function.
   - Choose **Python 3.x** as the runtime.
   - Copy and paste the Lambda function code into the editor.
   - Make sure to adjust the bucket name, base folder, and target folder if needed in the code.

4. **Set up the IAM role for the Lambda function**:
   - Attach the appropriate permissions to the Lambda execution role:
     - `s3:ListBucket`
     - `s3:GetObject`
     - `s3:PutObject`
   - You can create a new IAM role or use an existing one with these permissions.

5. **Configure the environment variables (if needed)**:
   - You can use environment variables in the AWS Lambda console to set values such as the bucket name, base folder, and target folder.

   Example environment variables:
   - `BUCKET_NAME`: `taza-datalake`
   - `BASE_FOLDER`: `raw/balance/public/`
   - `TARGET_FOLDER`: `balance_transaction/`

---

## Step 2: Create CloudWatch Event to Trigger Lambda Daily

1. **Go to CloudWatch** in the AWS Management Console.

2. **Create a new CloudWatch Rule**:
   - In **CloudWatch Events**, create a new rule to trigger the Lambda function on a schedule.
   - Set the rule to run daily at a specific time (e.g., midnight).
   - Attach the Lambda function as the target of the rule.

---

## Step 3: Testing the Lambda Function in AWS

1. **Upload files to S3**:
   - Upload files to the partitioned folders (e.g., `balance_transaction_2024_10/`) in your S3 bucket.

2. **Invoke the Lambda function**:
   - Either manually invoke the Lambda function from the console or let it trigger according to the scheduled CloudWatch event.

3. **Check CloudWatch Logs**:
   - Monitor the CloudWatch logs for the Lambda function to verify if the files were successfully moved to the `balance_transaction/` folder.

---

## Step 4: Verify Files in S3

1. Open the S3 Console and navigate to your bucket.

2. Check the `balance_transaction/` folder to confirm that the files from the partitioned folders have been copied.

3. Check the original partition folders to confirm that the files remain intact (no deletions).
