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

#Clear download folders, text file
folder = 'downloads'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
open('clips.txt', 'w').close()


f = open("clips.txt", "w")
for url in clip_urls:
	f.write(url + "\n")