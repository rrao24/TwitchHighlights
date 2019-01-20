def init():

	global CLIPS_URL
	CLIPS_URL = "https://api.twitch.tv/kraken/clips/top"

	global DOWNLOAD_CLIPS_URL
	DOWNLOAD_CLIPS_URL = "https://api.twitch.tv/helix/clips?id="

	global CLIP_PARAMS
	CLIP_PARAMS = {
	    "game": "Fortnite",
	    "period": "day",
	    "limit": 10,
	    "language": "en"
	}

	global CLIENT_ID
	CLIENT_ID = "bmqi273g9qwdztef0giu91l7150o25"

	global CLIP_HEADERS
	CLIP_HEADERS = {
	    "Accept": "application/vnd.twitchtv.v5+json",
	    "Client-ID": CLIENT_ID
	}

	global DOWNLOADS_FOLDER_NAME
	DOWNLOADS_FOLDER_NAME = 'downloads'

	global TRANSCODED_FOLDER_NAME
	TRANSCODED_FOLDER_NAME = 'transcoded_outputs'

	global TMP_FOLDERS
	TMP_FOLDERS = [DOWNLOADS_FOLDER_NAME, TRANSCODED_FOLDER_NAME]

	global FINAL_OUTPUTS_FOLDER_NAME
	FINAL_OUTPUTS_FOLDER_NAME = 'final_outputs'

	global CLIPS_FILE_NAME
	CLIPS_FILE_NAME = 'clips.txt'

	global YT_DESCRIPTION_FILE_NAME
	YT_DESCRIPTION_FILE_NAME = 'ytdescription.txt'

	global YT_DESCRIPTION_HEADER
	YT_DESCRIPTION_HEADER = 'Fortnite Stream Highlights\nCheck out the featured channels:\n'

	global VIDEO_QUALITY
	VIDEO_QUALITY = 22

	global BUCKET_NAME
	BUCKET_NAME = 'twitch-highlights'