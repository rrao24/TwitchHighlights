import lib.twitch as Twitch
import lib.filesystem as FileSystem
import lib.processing as Processing
import lib.s3 as S3
import globals

globals.init()

clips = Twitch.getTwitchClips()
clipUrls = Twitch.getClipUrls(clips)
broadcasterUrls = Twitch.getBroadcasterUrls(clips)
FileSystem.clearFolders()
FileSystem.writeClipUrls(clipUrls)
FileSystem.writeYTDescription(broadcasterUrls)
Twitch.downloadTwitchClips()
Processing.applyHandbrake()
fileName = Processing.mergeMP4()
S3.uploadToS3(fileName)