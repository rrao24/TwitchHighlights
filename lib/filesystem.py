import os

def getAllFilesInFolder(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and not f.startswith('.')]

def makeFolder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)

def clearFolder(folder):
    for theFile in os.listdir(folder):
        filePath = os.path.join(folder, theFile)
        if os.path.isfile(filePath):
            os.unlink(filePath)

def clearFile(file):
    open(file, 'w').close()

def writeYTDescription(broadcasterUrls, fileName, header):
    #write description to video
    ytDescription = header
    with open(fileName, 'w') as ytFile:
        for url in broadcasterUrls:
            ytDescription += url + "\n"
        ytFile.write(ytDescription)