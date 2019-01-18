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
	APP_NAME = 'mp4-merge'
	indir = globals.TRANSCODED_FOLDER_NAME + '/'
	outdir = globals.FINAL_OUTPUTS_FOLDER_NAME + '/'

	if not os.path.isdir(indir):
		indir = globals.DOWNLOADS_FOLDER_NAME

	if not os.path.isdir(outdir):
		os.makedirs(outdir)

	INPUT_EXT1 = '.MP4'
	OUT_EXT1 = '.mpg'
	date = datetime.datetime.today().strftime('%Y-%m-%d')
	MP4_RESULT_FILE = outdir + date + '-output.mp4'
	VIDEO_QUALITY = 22 #22=10300 Kbps, 23=, 24=6000 Kbps


	log = logging.getLogger(APP_NAME)
	log.setLevel(logging.DEBUG)
	lfh = logging.FileHandler(APP_NAME + '.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	lfh.setFormatter(formatter)
	log.addHandler(lfh)

	tmpdir = tempfile.mkdtemp()
	log.info('Temp dir ' + tmpdir)

	log.info('MP4s -> MPGs')
	mpg_file_list = list()
	for infile in os.listdir(indir):
		if infile.upper().endswith(INPUT_EXT1):
			outfile = tmpdir + '/' + infile + OUT_EXT1
			cmd = 'ffmpeg -i ' + indir + '/' + infile + ' -qscale:v 1 ' + outfile
			log.info(cmd)
			os.system(cmd)
			mpg_file_list.append(outfile)


	log.info('MPGs -> MP4')
	mpg_files_str = ''
	for mpg_file in mpg_file_list:
		mpg_files_str = mpg_files_str + mpg_file + '|'

	cmd = 'ffmpeg -i concat:"' + mpg_files_str + '" -c:v libx264 -preset slow -crf ' + str(VIDEO_QUALITY) + ' -c:a aac -strict -2 -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 ' + MP4_RESULT_FILE
	log.info(cmd)
	os.system(cmd)

	log.info('Removing temp dir ' + tmpdir + '...')
	shutil.rmtree(tmpdir)
	log.info('DONE')
	lfh.close()