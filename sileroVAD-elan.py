#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A short script to that wraps the SileroVAD voice activity detection
# package (https://github.com/snakers4/silero-vad) to act as a local
# recognizer in ELAN.
import torchaudio
import utils_vad
import re
import sys
import torch
from IPython.display import Audio
from pprint import pprint


print(str(torchaudio.get_audio_backend()))

SAMPLING_RATE = 16000

torch.set_num_threads(1)

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=False)

(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils


# Read in all of the parameters that ELAN passes to this local recognizer on
# standard input.
params = {}
for line in sys.stdin:
    match = re.search(r'<param name="(.*?)".*?>(.*?)</param>', line)
    if match:
        params[match.group(1)] = match.group(2).strip()


#read audio and extract timestamps
wav = read_audio(params["source"], sampling_rate=SAMPLING_RATE)
speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE, return_seconds=False)
pprint(speech_timestamps)

# Read in the amount of time users want to add/subtract from the start and
# end times of each of the segments produced by this recognizer.
adjust_start_s = float(params['adjust_start_ms']) / 1000.0
adjust_end_s = float(params['adjust_end_ms']) / 1000.0


# Then open 'output_segments' for writing, and return all of the new speech
# segments recognized by Silero as the contents of <span> elements.
with open(params['output_segments'], 'w', encoding = 'utf-8') as output_segs:
    # Write document header.
    output_segs.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output_segs.write('<TIER xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="file:avatech-tier.xsd" columns="SileroOutput">\n')
    for i in speech_timestamps:
        output_segs.write(\
            '    <span start="%.3f" end="%.3f"><v></v></span>\n' %\
            ((i['start'] / 16000), \
             (i['end'] / 16000)))
        print(i['start'] / 16000)
        print(i['end'] / 16000)
    output_segs.write('</TIER>\n')

# Finally, tell ELAN that we're done.
print('RESULT: DONE.', flush = True)
