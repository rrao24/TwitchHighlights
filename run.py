import lib.twitch as Twitch
import lib.filesystem as FileSystem
import lib.processing as Processing
import lib.s3 as S3
import os
import datetime
import globals

globals.init()

clips = Twitch.getTwitchClips(globals.CLIPS_URL, globals.CLIP_PARAMS, globals.CLIP_HEADERS)
clipUrls = Twitch.getClipUrls(clips)
broadcasterUrls = Twitch.getBroadcasterUrls(clips)

for folder in globals.TMP_FOLDERS:
	FileSystem.clearFolder(folder)
for file in globals.TMP_FILES:
	FileSystem.clearFile(file)

FileSystem.writeClipUrls(clipUrls, globals.CLIPS_FILE_NAME)
FileSystem.writeYTDescription(broadcasterUrls, globals.YT_DESCRIPTION_FILE_NAME, globals.YT_DESCRIPTION_HEADER)

Twitch.downloadTwitchClips(globals.CLIPS_FILE_NAME, globals.DOWNLOADS_FOLDER_NAME + '/', globals.DOWNLOAD_CLIPS_URL, globals.CLIENT_ID)

Processing.applyHandbrake(globals.DOWNLOADS_FOLDER_NAME, globals.TRANSCODED_FOLDER_NAME)
fileName = Processing.mergeMP4(globals.TRANSCODED_FOLDER_NAME + '/', globals.FINAL_OUTPUTS_FOLDER_NAME + '/', globals.VIDEO_QUALITY)

clips = [f for f in os.listdir(globals.TRANSCODED_FOLDER_NAME) if os.path.isfile(os.path.join(globals.TRANSCODED_FOLDER_NAME, f)) and not f.startswith('.')]
date = datetime.datetime.today().strftime('%Y-%m-%d')
for clip in clips:
	S3.uploadToS3(globals.TRANSCODED_FOLDER_NAME + '/' + clip, globals.OUTPUTS_BUCKET_NAME, 'clips' + '/' + date + '/' + clip)
S3.uploadToS3(fileName, globals.OUTPUTS_BUCKET_NAME, fileName)