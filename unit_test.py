import unittest
from unittest.mock import patch, MagicMock
from moto import mock_s3
import boto3

class TestLambdaFunction(unittest.TestCase):

    @mock_s3
    def setUp(self):
        # Setup mock S3 environment
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = 'taza-datalake'
        self.base_folder = 'raw/balance/public/'
        self.target_folder = 'balance_transaction/'
        self.partition_folder = 'balance_transaction_2024_09/'
        
        # Create mock bucket and add files
        self.s3.create_bucket(Bucket=self.bucket_name)
        self.s3.put_object(Bucket=self.bucket_name, Key=f'{self.base_folder}{self.partition_folder}file1.csv', Body='data1')
        self.s3.put_object(Bucket=self.bucket_name, Key=f'{self.base_folder}{self.partition_folder}file2.csv', Body='data2')

    @mock_s3
    @patch('lambda_function.s3')
    def test_move_files(self, mock_s3):
        """Test if files are moved from partition to target folder"""
        
        # Mock the S3 client
        mock_s3.list_objects_v2.return_value = {
            'Contents': [
                {'Key': f'{self.base_folder}{self.partition_folder}file1.csv'},
                {'Key': f'{self.base_folder}{self.partition_folder}file2.csv'}
            ]
        }
        
        # Execute function
        from lambda_function import move_files_from_folder
        
        move_files_from_folder(self.bucket_name, self.base_folder, self.partition_folder, self.target_folder)
        
        # Check if the files are copied to the target folder
        copied_file1 = self.s3.head_object(Bucket=self.bucket_name, Key=f'{self.base_folder}{self.target_folder}file1.csv')
        copied_file2 = self.s3.head_object(Bucket=self.bucket_name, Key=f'{self.base_folder}{self.target_folder}file2.csv')
        
        self.assertIsNotNone(copied_file1)
        self.assertIsNotNone(copied_file2)

    @mock_s3
    def test_file_exists(self):
        """Test file existence checker"""
        
        from lambda_function import file_exists
        
        # Check for an existing file
        self.assertTrue(file_exists(self.bucket_name, f'{self.base_folder}{self.partition_folder}file1.csv'))
        
        # Check for a non-existent file
        self.assertFalse(file_exists(self.bucket_name, f'{self.base_folder}{self.partition_folder}non_existent_file.csv'))

if __name__ == '__main__':
    unittest.main()
