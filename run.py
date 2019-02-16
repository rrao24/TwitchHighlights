import lib.twitch as Twitch
import lib.filesystem as FileSystem
import lib.processing as Processing
import lib.s3 as S3
import globals

globals.init()

clips = Twitch.getTwitchClips(clipsUrl=globals.CLIPS_URL,
	clipParams=globals.CLIP_PARAMS,
	clipHeaders=globals.CLIP_HEADERS,
	minsDiffForDuplicateDetection=globals.MINS_DIFF_FOR_DUPLICATE_DETECTION)
clipUrls = Twitch.getClipUrls(clips)
broadcasterUrls = Twitch.getBroadcasterUrls(clips)

FileSystem.makeFolder(globals.DOWNLOADS_FOLDER_NAME)
FileSystem.makeFolder(globals.TRANSCODED_FOLDER_NAME)
FileSystem.makeFolder(globals.FINAL_OUTPUTS_FOLDER_NAME)
for folder in globals.TMP_FOLDERS:
	FileSystem.clearFolder(folder)
FileSystem.clearFile(globals.YT_DESCRIPTION_FILE_NAME)

FileSystem.writeYTDescription(broadcasterUrls=broadcasterUrls,
	fileName=globals.YT_DESCRIPTION_FILE_NAME,
	header=globals.YT_DESCRIPTION_HEADER)

Twitch.downloadTwitchClips(clipUrls=clipUrls,
	toFile=globals.DOWNLOADS_FOLDER_NAME + '/',
	downloadClipsUrl=globals.DOWNLOAD_CLIPS_URL,
	clientID=globals.CLIENT_ID)

clips = FileSystem.getAllFilesInFolder(globals.DOWNLOADS_FOLDER_NAME)
Processing.applyHandbrake(indir=globals.DOWNLOADS_FOLDER_NAME, clips=clips, outdir=globals.TRANSCODED_FOLDER_NAME)

clips = FileSystem.getAllFilesInFolder(globals.TRANSCODED_FOLDER_NAME)
fileName = Processing.mergeMP4(indir=globals.TRANSCODED_FOLDER_NAME + '/',
	clips=clips,
	outdir=globals.FINAL_OUTPUTS_FOLDER_NAME + '/',
	videoQuality=globals.VIDEO_QUALITY,
	date=globals.DATE)

clips = FileSystem.getAllFilesInFolder(globals.TRANSCODED_FOLDER_NAME)
for clip in clips:
	S3.uploadToS3(inFile=globals.TRANSCODED_FOLDER_NAME + '/' + clip,
		bucketName=globals.OUTPUTS_BUCKET_NAME,
		outFile='clips' + '/' + globals.DATE + '/' + clip)
S3.uploadToS3(inFile=fileName, bucketName=globals.OUTPUTS_BUCKET_NAME, outFile=fileName)
S3.uploadToS3(inFile=globals.YT_DESCRIPTION_FILE_NAME, bucketName=globals.OUTPUTS_BUCKET_NAME, outFile='descriptions' + '/' + globals.DATE + '/' + globals.YT_DESCRIPTION_FILE_NAME)