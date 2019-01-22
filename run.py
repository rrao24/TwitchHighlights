import lib.twitch as Twitch
import lib.filesystem as FileSystem
import lib.processing as Processing
import lib.s3 as S3
import os
import globals

globals.init()

clips = Twitch.getTwitchClips(clipsUrl=globals.CLIPS_URL,
	clipParams=globals.CLIP_PARAMS,
	clipHeaders=globals.CLIP_HEADERS,
	minsDiffForDuplicateDetection=globals.MINS_DIFF_FOR_DUPLICATE_DETECTION)
clipUrls = Twitch.getClipUrls(clips)
broadcasterUrls = Twitch.getBroadcasterUrls(clips)

for folder in globals.TMP_FOLDERS:
	FileSystem.clearFolder(folder)
for file in globals.TMP_FILES:
	FileSystem.clearFile(file)

FileSystem.writeClipUrls(clipUrls=clipUrls, fileName=globals.CLIPS_FILE_NAME)
FileSystem.writeYTDescription(broadcasterUrls=broadcasterUrls,
	fileName=globals.YT_DESCRIPTION_FILE_NAME,
	header=globals.YT_DESCRIPTION_HEADER)

Twitch.downloadTwitchClips(inFile=globals.CLIPS_FILE_NAME,
	toFile=globals.DOWNLOADS_FOLDER_NAME + '/',
	downloadClipsUrl=globals.DOWNLOAD_CLIPS_URL,
	clientID=globals.CLIENT_ID)

Processing.applyHandbrake(indir=globals.DOWNLOADS_FOLDER_NAME, outdir=globals.TRANSCODED_FOLDER_NAME)
fileName = Processing.mergeMP4(indir=globals.TRANSCODED_FOLDER_NAME + '/',
	outdir=globals.FINAL_OUTPUTS_FOLDER_NAME + '/',
	videoQuality=globals.VIDEO_QUALITY,
	date=globals.DATE)

clips = [f for f in os.listdir(globals.TRANSCODED_FOLDER_NAME) if os.path.isfile(os.path.join(globals.TRANSCODED_FOLDER_NAME, f)) and not f.startswith('.')]
for clip in clips:
	S3.uploadToS3(inFile=globals.TRANSCODED_FOLDER_NAME + '/' + clip,
		bucketName=globals.OUTPUTS_BUCKET_NAME,
		outFile='clips' + '/' + globals.DATE + '/' + clip)
S3.uploadToS3(inFile=fileName, bucketName=globals.OUTPUTS_BUCKET_NAME, outFile=fileName)