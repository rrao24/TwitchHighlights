import os
import sys
import tempfile
import shutil
import logging
import datetime

APP_NAME = 'mp4-merge'
indir = 'transcoded_outputs/'
outdir = 'final_outputs/'

if not os.path.isdir('transcoded_outputs'):
    indir = 'downloads/'
    
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