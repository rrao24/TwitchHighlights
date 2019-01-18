import lib.twitch as Twitch
import lib.filesystem as FileSystem
import lib.processing as Processing
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
Processing.mergeMP4()