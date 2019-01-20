import subprocess
from os import listdir
from os.path import isfile, join
import os
import sys
import tempfile
import shutil
import logging
import datetime
import globals

def applyHandbrake():
	clips = [f for f in listdir(globals.DOWNLOADS_FOLDER_NAME) if isfile(join(globals.DOWNLOADS_FOLDER_NAME, f)) and not f.startswith('.')]

	for clip in clips:
		inClip = globals.DOWNLOADS_FOLDER_NAME + '/' + clip
		outClip = globals.TRANSCODED_FOLDER_NAME + '/' + clip
		print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))

def mergeMP4():
	indir = globals.TRANSCODED_FOLDER_NAME + '/'
	outdir = globals.FINAL_OUTPUTS_FOLDER_NAME + '/'

	if not os.path.isdir(indir) or not os.listdir(indir):
		indir = globals.DOWNLOADS_FOLDER_NAME + '/'

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

	cmd = 'ffmpeg -i concat:"' + mpg_files_str + '" -use_wallclock_as_timestamps 1 -c:v libx264 -preset slow -crf ' + str(globals.VIDEO_QUALITY) + ' -c:a aac -strict -2 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + MP4_RESULT_FILE
	os.system(cmd)

	shutil.rmtree(tmpdir)
	return MP4_RESULT_FILE