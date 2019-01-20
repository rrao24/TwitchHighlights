import boto3
from os import listdir
from os.path import isfile, join
import os
import datetime
import globals

def uploadToS3(fileName):
	clipsdir = globals.TRANSCODED_FOLDER_NAME + '/'
	if not os.path.isdir(clipsdir) or not os.listdir(clipsdir):
		clipsdir = globals.DOWNLOADS_FOLDER_NAME + '/'
	clips = [f for f in listdir(clipsdir) if isfile(join(clipsdir, f)) and not f.startswith('.')]
	date = datetime.datetime.today().strftime('%Y-%m-%d')
	outputsBucketName = globals.OUTPUTS_BUCKET_NAME

	client = boto3.client('s3')
	for clip in clips:
		client.upload_file(clipsdir + clip, outputsBucketName, 'clips' + '/' + date + '/' + clip)

	client.upload_file(fileName, outputsBucketName, fileName)