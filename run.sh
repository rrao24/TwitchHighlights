#!/bin/sh

python pipe.py
python batchloader.py "bmqi273g9qwdztef0giu91l7150o25"
python transcode.py
python concat.py