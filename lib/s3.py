import boto3

def uploadToS3(inFile, bucketName, outFile):
	client = boto3.client('s3')
	client.upload_file(inFile, bucketName, outFile)