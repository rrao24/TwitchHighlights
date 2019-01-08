import subprocess
from os import listdir
from os.path import isfile, join
from vidpy import Clip, Composition
import datetime

clips = [f for f in listdir('downloads') if isfile(join('downloads', f)) and not f.startswith('.')]
date = datetime.datetime.today().strftime('%Y-%m-%d')
output_str = 'final_outputs/' + date + '-output.mp4'
broadcasters_f = open("broadcasters.txt", "r")
broadcasters = [broadcaster for broadcaster in broadcasters_f]

for clip in clips:
	inClip = 'downloads/' + clip
	outClip = 'transcoded_outputs/' + clip
	print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))

clip_objects = [Clip('transcoded_outputs/' + f) for f in listdir('transcoded_outputs') if isfile(join('transcoded_outputs', f)) and not f.startswith('.')]
counter = 0
for clip_object in clip_objects:
	clip_object.fadeout(0.2)
	counter += 1
clip_objects_iter = iter(clip_objects)
next(clip_objects_iter)
for clip_object in clip_objects_iter:
	clip_object.fadein(0.2)
composition = Composition(clip_objects, singletrack=True)
composition.save(output_str)