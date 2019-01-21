import os

def clearFolder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

def clearFile(file):
    open(file, 'w').close()

def writeClipUrls(clipUrls, fileName):
    #write file of clip urls to download
    with open(fileName, "w") as clipFile:
        for url in clipUrls:
            clipFile.write(url + "\n")

def writeYTDescription(broadcasterUrls, fileName, header):
    #write description to video
    ytDescription = header
    with open(fileName, 'w') as ytFile:
        for url in broadcasterUrls:
            ytDescription += url + "\n"
        ytFile.write(ytDescription)