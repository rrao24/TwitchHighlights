import subprocess
import os
import tempfile
import shutil
import datetime

def applyHandbrake(indir, clips, outdir):
	for clip in clips:
		inClip = indir + '/' + clip
		outClip = outdir + '/' + clip
		print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))

def mergeMP4(indir, outdir, videoQuality, date):
	mp4ResultFile = outdir + date + '-output.mp4'
	tmpdir = tempfile.mkdtemp()

	mpgFileList = list()
	for infile in os.listdir(indir):
		if infile.upper().endswith('.MP4'):
			outfile = tmpdir + '/' + infile + '.mpg'
			cmd = 'ffmpeg -i ' + indir + '/' + infile + ' -qscale:v 1 ' + outfile
			os.system(cmd)
			mpgFileList.append(outfile)

	mpgFilesStr = ''
	for mpgFile in mpgFileList:
		mpgFilesStr = mpgFilesStr + mpgFile + '|'

	cmd = 'ffmpeg -i concat:"' + mpgFilesStr + '" -use_wallclock_as_timestamps 1 -c:v libx264 -preset slow -crf ' + str(videoQuality) + ' -c:a aac -strict -2 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + mp4ResultFile
	os.system(cmd)

	shutil.rmtree(tmpdir)
	return mp4ResultFile