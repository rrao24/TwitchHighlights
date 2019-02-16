import os
import tempfile
import shutil

def applyHandbrake(indir, clips, outdir):
	for clip in clips:
		inClip = indir + '/' + clip
		outClip = outdir + '/' + clip
		cmd = './HandBrakeCLI -i ' + inClip + ' -o ' + outClip
		os.system(cmd)

def mergeMP4(indir, clips, outdir, videoQuality, date):
	mp4ResultFile = outdir + date + '-output.mp4'
	tmpdir = tempfile.mkdtemp()

	mpgFileList = []
	for clip in clips:
		outfile = tmpdir + '/' + clip + '.mpg'
		cmd = 'ffmpeg -i ' + indir + clip + ' -qscale:v 1 ' + outfile
		os.system(cmd)
		mpgFileList.append(outfile)

	mpgFilesStr = ''
	for mpgFile in mpgFileList:
		mpgFilesStr = mpgFilesStr + mpgFile + '|'

	cmd = 'ffmpeg -i concat:"' + mpgFilesStr + '" -use_wallclock_as_timestamps 1 -c:v libx264 -preset slow -crf ' + str(videoQuality) + ' -c:a aac -strict -2 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + mp4ResultFile
	os.system(cmd)

	shutil.rmtree(tmpdir)
	return mp4ResultFile