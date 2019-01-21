import requests
import datetime
import re
import urllib.request
import sys

def getTwitchClips(clipsUrl, clipParams, clipHeaders):
	request = requests.get(clipsUrl, params=clipParams, headers=clipHeaders)
	clips = request.json()["clips"]
	nonDuplicateClips = removeDuplicateClips(clips)
	return nonDuplicateClips

def removeDuplicateClips(clips):
	#parse appropriate information
	tmpClips = []

	for clip in clips:
		tmpClips.append({
		'broadcaster': clip['broadcaster']['display_name'],
		'broadcasterUrl': clip['broadcaster']['channel_url'],
		'created_at': datetime.datetime.strptime(clip['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
		'url': clip['url'],
		'duplicate': False
		})

	#remove duplicates
	nonDuplicateClips = []

	for i in range(len(tmpClips)):
		for j in range(i + 1, len(tmpClips)):
			minsDiff = abs((tmpClips[i]['created_at'] - tmpClips[j]['created_at']).days * 24 * 60)
			sameStreamer = tmpClips[i]['broadcaster'] == tmpClips[j]['broadcaster']
			if sameStreamer and minsDiff < 30:
				tmpClips[i]['duplicate'] = True
				break
		if tmpClips[i]['duplicate'] == False:
			nonDuplicateClips.append(tmpClips[i])

	return nonDuplicateClips

def getClipUrls(clips):
	clipUrls = [ clip["url"].split("?")[0] for clip in clips ]
	return clipUrls

def getBroadcasterUrls(clips):
	#cite broadcasters
	broadcasterUrls = [clip["broadcasterUrl"] for clip in clips]
	broadcasterUrlsUnique = list(set(broadcasterUrls))
	return broadcasterUrlsUnique

def downloadTwitchClips(inFile, toFile, downloadClipsUrl, clientID):
	# for each clip in clips.txt
	with open(inFile, 'r') as read_clips:
		for clip in read_clips:
			slug = clip.split('/')[3].replace('\n', '')
			mp4_url, clip_title = retrieve_mp4_data(slug, downloadClipsUrl, clientID)
			regex = re.compile('[^a-zA-Z0-9_]')
			clip_title = clip_title.replace(' ', '_')
			out_filename = regex.sub('', clip_title) + '.mp4'
			output_path = (toFile + out_filename)

			print('\nDownloading clip slug: ' + slug)
			print('"' + clip_title + '" -> ' + out_filename)
			print(mp4_url)
			urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
			print('\nDone.')


def retrieve_mp4_data(slug, downloadClipsUrl, clientID):
	clip_info = requests.get(
	    downloadClipsUrl + slug,
	    headers={"Client-ID": clientID}).json()
	thumb_url = clip_info['data'][0]['thumbnail_url']
	title = clip_info['data'][0]['title']
	slice_point = thumb_url.index("-preview-")
	mp4_url = thumb_url[:slice_point] + '.mp4'
	return mp4_url, title


def dl_progress(count, block_size, total_size):
	percent = int(count * block_size * 100 / total_size)
	sys.stdout.write("\r...%d%%" % percent)
	sys.stdout.flush()