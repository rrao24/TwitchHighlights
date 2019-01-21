import subprocess
import os
import tempfile
import shutil
import datetime

def applyHandbrake(indir, outdir):
	clips = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f)) and not f.startswith('.')]

	for clip in clips:
		inClip = indir + '/' + clip
		outClip = outdir + '/' + clip
		print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))

def mergeMP4(indir, outdir, videoQuality):
	if not os.path.isdir(outdir):
		os.makedirs(outdir)

	INPUT_EXT1 = '.MP4'
	OUT_EXT1 = '.mpg'
	date = datetime.datetime.today().strftime('%Y-%m-%d')
	MP4_RESULT_FILE = outdir + date + '-output.mp4'

	tmpdir = tempfile.mkdtemp()

	mpg_file_list = list()
	for infile in os.listdir(indir):
		if infile.upper().endswith(INPUT_EXT1):
			outfile = tmpdir + '/' + infile + OUT_EXT1
			cmd = 'ffmpeg -i ' + indir + '/' + infile + ' -qscale:v 1 ' + outfile
			os.system(cmd)
			mpg_file_list.append(outfile)

	mpg_files_str = ''
	for mpg_file in mpg_file_list:
		mpg_files_str = mpg_files_str + mpg_file + '|'

	cmd = 'ffmpeg -i concat:"' + mpg_files_str + '" -use_wallclock_as_timestamps 1 -c:v libx264 -preset slow -crf ' + str(videoQuality) + ' -c:a aac -strict -2 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + MP4_RESULT_FILE
	os.system(cmd)

	shutil.rmtree(tmpdir)
	return MP4_RESULT_FILE