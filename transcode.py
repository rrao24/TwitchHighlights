import subprocess
from os import listdir
from os.path import isfile, join

clips = [f for f in listdir('downloads') if isfile(join('downloads', f)) and not f.startswith('.')]

for clip in clips:
	inClip = 'downloads/' + clip
	outClip = 'transcoded_outputs/' + clip
	print(subprocess.check_output(['./HandBrakeCLI', '-i', inClip, '-o', outClip]))