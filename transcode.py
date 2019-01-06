import subprocess
from os import listdir
from os.path import isfile, join
from vidpy import Clip, Composition
import datetime

clips = [f for f in listdir('downloads') if isfile(join('downloads', f)) and not f.startswith('.')]
date = datetime.datetime.today().strftime('%Y-%m-%d')
output_str = 'final_outputs/' + date + '-output.mp4'

for clip in clips:
	inClip = 'downloads/' + clip
	outClip = 'transcoded_outputs/' + clip
	print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))

clip_objects = [Clip('transcoded_outputs/' + f) for f in listdir('transcoded_outputs') if isfile(join('transcoded_outputs', f)) and not f.startswith('.')]
composition = Composition(clip_objects, singletrack=True)
composition.save(output_str)