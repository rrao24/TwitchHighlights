import boto3

def uploadToS3(inFile, bucketName, outFile, awsId, awsSecret):
	client = boto3.client('s3', aws_access_key_id=awsId, aws_secret_access_key=awsSecret)
	client.upload_file(inFile, bucketName, outFile)