import requests
import os
import shutil
import datetime

date_today = datetime.datetime.today().strftime('%Y-%m-%d')
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

#request clips
request = requests.get(clips_url, params=clip_params, headers=clip_headers)
clips = request.json()["clips"]

#parse appropriate information
tmpClips = []

for clip in clips:
    tmpClips.append({
        'broadcaster': clip['broadcaster']['display_name'],
        'created_at': datetime.datetime.strptime(clip['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
        'url': clip['url'],
        'duplicate': False
        })
    print(clip['broadcaster']['display_name'])

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

#cite broadcasters
clip_urls = [ clip["url"].split("?")[0] for clip in nonDuplicateClips ]
broadcaster_urls = [clip["broadcaster"]['channel_url'] for clip in clips]
broadcaster_urls_uniq = list(set(broadcaster_urls))

#Clear download folders, text file
folders = ['downloads', 'transcoded_outputs']
for folder in folders:
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

#write file of clip urls to download
with open("clips.txt", "w") as clip_f:
    for url in clip_urls:
        clip_f.write(url + "\n")
        
#write description to video
with open('ytdescription.txt', 'w') as yt_f:
    yt_description = "Fortnite Stream Highlights\nCheck out the featured channels:\n"
    for url in broadcaster_urls_uniq:
        yt_description += url + "\n"
    yt_f.write(yt_description)

#write list of broadcasters
with open('broadcasters.txt', 'w') as broadcaster_f:
    for broadcaster_url in broadcaster_urls:
        broadcaster_f.write(broadcaster_url + "\n")

broadcaster_f = open('broadcasters.txt', 'w')
for broadcaster_url in broadcaster_urls:
    broadcaster_f.write(broadcaster_url + "\n")