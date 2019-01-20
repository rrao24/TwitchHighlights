import boto3
import globals

def uploadToS3(fileName):
	bucketName = globals.BUCKET_NAME
	client = boto3.client('s3')
	response = client.upload_file(fileName, bucketName, fileName)