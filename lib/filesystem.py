import os
import globals

def clearFolders():
    #Clear download folders, text file
    for folder in globals.TMP_FOLDERS:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    open(globals.CLIPS_FILE_NAME, 'w').close()
    open(globals.YT_DESCRIPTION_FILE_NAME, 'w').close()

def writeClipUrls(clipUrls):
    #write file of clip urls to download
    with open(globals.CLIPS_FILE_NAME, "w") as clip_f:
        for url in clipUrls:
            clip_f.write(url + "\n")

def writeYTDescription(broadcasterUrls):
    #write description to video
    yt_description = globals.YT_DESCRIPTION_HEADER
    with open(globals.YT_DESCRIPTION_FILE_NAME, 'w') as yt_f:
        for url in broadcasterUrls:
            yt_description += url + "\n"
        yt_f.write(yt_description)