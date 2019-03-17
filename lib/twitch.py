import requests
import datetime
import re
import urllib.request
import sys
import time

def getTwitchClips(clipsUrl, clipParams, clipHeaders, minsDiffForDuplicateDetection, numClips, whiteListFile):
	request = requests.get(clipsUrl, params=clipParams, headers=clipHeaders)
	clips = request.json()["clips"]
	nonDuplicateClips = removeDuplicateClips(clips, minsDiffForDuplicateDetection)
	whiteListedClips = applyWhiteList(nonDuplicateClips, numClips, whiteListFile)
	return whiteListedClips

def applyWhiteList(clips, numClips, whiteListFile):
	whiteListedClips = []
	whiteList = open(whiteListFile, 'r').read().splitlines()
	whiteList = [broadcaster.lower() for broadcaster in whiteList]
	for clip in clips:
		if clip['broadcaster'].lower() in whiteList:
			whiteListedClips.append(clip)
	return whiteListedClips[:numClips]

def removeDuplicateClips(clips, minsDiffForDuplicateDetection):
	#parse appropriate information
	tmpClips = []

	fmt = "%Y-%m-%dT%H:%M:%SZ"
	for clip in clips:
		tmpClips.append({
		'broadcaster': clip['broadcaster']['name'],
		'broadcasterUrl': clip['broadcaster']['channel_url'],
		'created_at': time.mktime(datetime.datetime.strptime(clip['created_at'], fmt).timetuple()),
		'url': clip['url'],
		'duplicate': False
		})

	#remove duplicates
	nonDuplicateClips = []

	for i in range(len(tmpClips)):
		for j in range(i + 1, len(tmpClips)):
			minsDiff = abs((tmpClips[i]['created_at'] - tmpClips[j]['created_at']) / 60)
			sameStreamer = tmpClips[i]['broadcaster'] == tmpClips[j]['broadcaster']
			if sameStreamer and minsDiff < minsDiffForDuplicateDetection:
				tmpClips[i]['duplicate'] = True
				break
		if tmpClips[i]['duplicate'] == False:
			nonDuplicateClips.append(tmpClips[i])

	return nonDuplicateClips

def getClipUrls(clips):
	clipUrls = [clip["url"].split("?")[0] for clip in clips]
	return clipUrls

def getBroadcasterUrls(clips):
	#cite broadcasters
	broadcasterUrls = [clip["broadcasterUrl"] for clip in clips]
	broadcasterUrlsUnique = list(set(broadcasterUrls))
	return broadcasterUrlsUnique

def downloadTwitchClips(clipUrls, toFile, downloadClipsUrl, clientID):
	# for each clip in clips.txt
	for clip in clipUrls:
		slug = clip.split('/')[3].replace('\n', '')
		mp4Url, clipTitle = retrieveMp4Data(slug, downloadClipsUrl, clientID)
		regex = re.compile('[^a-zA-Z0-9_]')
		clipTitle = clipTitle.replace(' ', '_')
		outFilename = regex.sub('', clipTitle) + '.mp4'
		outputPath = (toFile + outFilename)

		print('\nDownloading clip slug: ' + slug)
		print('"' + clipTitle + '" -> ' + outFilename)
		print(mp4Url)
		urllib.request.urlretrieve(mp4Url, outputPath, reporthook=dlProgress)
		print('\nDone.')


def retrieveMp4Data(slug, downloadClipsUrl, clientID):
	clipInfo = requests.get(
	    downloadClipsUrl + slug,
	    headers={"Client-ID": clientID}).json()
	thumbUrl = clipInfo['data'][0]['thumbnail_url']
	title = clipInfo['data'][0]['title']
	slicePoint = thumbUrl.index("-preview-")
	mp4Url = thumbUrl[:slicePoint] + '.mp4'
	return mp4Url, title


def dlProgress(count, blockSize, totalSize):
	percent = int(count * blockSize * 100 / totalSize)
	sys.stdout.write("\r...%d%%" % percent)
	sys.stdout.flush()