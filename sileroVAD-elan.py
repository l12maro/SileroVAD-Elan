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
# end times of each of the segments produced by this recognizer.  (A quick-
# and-dirty way of working around results that may clip the starts or ends
# of annotations, but are otherwise fine)
adjust_start_s = float(params['adjust_start_ms']) / 1000.0
adjust_end_s = float(params['adjust_end_ms']) / 1000.0

# Since Voxseg often misses the starts of segments (particularly noisy
# consonants like /s/), we allow users the option of applying a post-hoc,
# silence-detection-based adjustment to the beginnings and ends of the
# segments that Voxseg returns.
#
# In practical terms, this involves moving a sliding window (by default,
# 10ms wide) running over an additional bit (by default, 250ms) over audio
# shortly before and after the start and end of each segment, seeing if
# that audio exceeds a user-specified volume threshold (by default,
# relative to the volume of the segment itself).
#
# We also use pydub's silence detection facilities to detect longer periods
# of silence within the segments that Voxseg returns -- it tends to return
# quite large chunks on its own, and we can often find smaller chunks within
# those that are separated by (near) silence.
"""
do_silence_detection = (params['do_silence_detection'] == 'Enable')
if do_silence_detection:
    audio = pydub.AudioSegment.from_wav(tmp_wav_file)

    search_window_ms = 250
    window_ms = 10
    edge_threshold_factor = 1.0 + (float(params['edge_threshold']) / 100)
    internal_threshold_factor = 1.0+(float(params['internal_threshold']) / 100)

    adjusted_labels = [dict(\
        [('start', int(predicted_labels['start'][i] * 1000)), \
         ('end', int(predicted_labels['end'][i] * 1000))]) \
           for i in predicted_labels.index]

    for i in range(len(adjusted_labels)):
        orig_start_ms = adjusted_labels[i]['start']
        orig_end_ms = adjusted_labels[i]['end']
        orig_clip = audio[orig_start_ms:orig_end_ms]
        orig_avg_vol = orig_clip.dBFS
        threshold_vol = orig_clip.dBFS * edge_threshold_factor

        # Now, starting from $search_window_ms before the original start time
        # for this segment, step in $window_ms increments over the audio,
        # checking to see whether or not this snippet falls above or below
        # the volume threshold (relative to the average volume of the original
        # segment).
        new_start_ms = max(0, orig_start_ms - search_window_ms)
        for window in range(new_start_ms, orig_end_ms, window_ms):
            window_clip = audio[window:window + window_ms]
            window_clip_avg_vol = window_clip.dBFS

            # If we're under or at the threshold, then treat this window as
            # silence and adjust the start time of this segment accordingly.
            if window_clip_avg_vol <= threshold_vol:
                adjusted_labels[i]['start'] = window
            # Otherwise, if we're over the threshold, then this window contains
            # non-silence, and we should stop where we are and quit trying to
            # adjust the start times for this segment.
            else:
                adjusted_labels[i]['start'] = window - window_ms
                break

        # Now apply the same logic to the end of the segment, stepping back-
        # wards in $window_ms increments to see where our relative volume
        # threshold is exceeded (and adjusting the end of this segment up to
        # that point).
        new_end_ms = min(orig_end_ms + search_window_ms, len(audio)) 
        for window in range(new_end_ms - window_ms, \
                            adjusted_labels[i]['start'], -window_ms):
            window_clip = audio[window:window + window_ms]
            window_clip_avg_vol = window_clip.dBFS

            if window_clip_avg_vol <= threshold_vol:
                adjusted_labels[i]['end'] = window
            else:
#                adjusted_labels[i]['end'] = window + window_ms
                adjusted_labels[i]['end'] = window
                break

    # Now look for longer periods of silence *within* these segments, splitting
    # up longer segments into smaller sections of non-silence.
    split_labels = []
    keep_silence_ms = 50
    for i in range(len(adjusted_labels)):
        start_ms = adjusted_labels[i]['start']
        end_ms = adjusted_labels[i]['end']

        clip = audio[start_ms:end_ms]
        avg_vol = clip.dBFS
        threshold_vol = avg_vol * internal_threshold_factor

        segs = pydub.silence.detect_nonsilent(clip, min_silence_len = 500, \
            silence_thresh = threshold_vol, seek_step = 10)

        for (i, [seg_start_ms, seg_end_ms]) in enumerate(segs):
            # Keep a bit of silence on either end of each of the new segments.
            if i != 0:
                seg_start_ms -= keep_silence_ms
            if i != len(segs) - 1:
                seg_end_ms += keep_silence_ms

            split_labels.append(dict(\
                [('start', start_ms + seg_start_ms), \
                 ('end', start_ms + seg_end_ms)]))

    adjusted_labels = split_labels
"""


# Then open 'output_segments' for writing, and return all of the new speech
# segments recognized by Voxseg as the contents of <span> elements (see
# below).
with open(params['output_segments'], 'w', encoding = 'utf-8') as output_segs:
    # Write document header.
    output_segs.write('<?xml version="1.0" encoding="UTF-8"?>\n')

    # Write out the adjusted annotations if the user requested that silence
    # detection be applied.
#    if do_silence_detection:
#        output_segs.write('<TIER xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="file:avatech-tier.xsd" columns="VoxsegOutput-Adjusted">\n')
#        for a in adjusted_labels:
#            output_segs.write(\
#                '    <span start="%.3f" end="%.3f"><v></v></span>\n' %\
#                ((a['start'] / 1000.0) + adjust_start_s, \
#                 (a['end'] / 1000.0) + adjust_end_s))

#        output_segs.write('</TIER>\n')
    # Otherwise, just write out whatever Voxseg gave us (with any user-
    # specified adjustments to the start and end times of each segment).
#    else:
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
