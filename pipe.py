import requests
import os
import shutil
import datetime

clips_url = "https://api.twitch.tv/kraken/clips/top"

clip_params = {
	"game": "Fortnite",
	"period": "day",
	"limit": 10,
	"language": "en"
}

clip_headers = {
	"Accept": "application/vnd.twitchtv.v5+json",
	"Client-ID": "bmqi273g9qwdztef0giu91l7150o25"
}

request = requests.get(clips_url, params=clip_params, headers=clip_headers)
clips = request.json()["clips"]

tmpClips = []

for clip in clips:
	tmpClips.append({
		'broadcaster': clip['broadcaster']['display_name'],
		'created_at': datetime.datetime.strptime(clip['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
		'url': clip['url'],
		'duplicate': False
		})
	print(clip['broadcaster']['display_name'])

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

clip_urls = [ clip["url"].split("?")[0] for clip in nonDuplicateClips ]
broadcaster_urls = [clip["broadcaster"]['channel_url'] for clip in clips]
broadcaster_urls_uniq = list(set(broadcaster_urls))

#Clear download folders, text file
folders = ['downloads', 'transcoded_outputs']
for folder in folders:
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    if os.path.isfile(file_path):
	        os.unlink(file_path)
open('clips.txt', 'w').close()
open('ytdescription.txt', 'w').close()
open('broadcasters.txt', 'w').close()

f = open("clips.txt", "w")
for url in clip_urls:
	f.write(url + "\n")

yt_description = "Fortnite Stream Highlights\nCheck out the featured channels:\n"
for url in broadcaster_urls_uniq:
	yt_description += url + "\n"
yt_f = open('ytdescription.txt', 'w')
yt_f.write(yt_description)

broadcaster_f = open('broadcasters.txt', 'w')
for broadcaster_url in broadcaster_urls:
	broadcaster_f.write(broadcaster_url + "\n")
