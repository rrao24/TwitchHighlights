import requests
import os
import shutil

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

clip_urls = [ clip["url"].split("?")[0] for clip in clips ]
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
