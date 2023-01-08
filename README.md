# SileroVAD-ELAN 0.1.1

SileroVAD-ELAN integrates the voice activity detection methods offered by
[Silero-Vad](https://github.com/snakers4/silero-vad) (Silero Team 2021) into 
[ELAN](https://tla.mpi.nl/tools/tla-tools/elan/), allowing users to apply
voice activity detection to multimedia sources linked to ELAN transcripts
directly from within ELAN's user interface.

## Requirements and installation

SileroVAD-ELAN makes use of several of other open-source applications and
utilities:

* [ELAN](https://tla.mpi.nl/tools/tla-tools/elan/) (tested with ELAN 6.3
  and 6.4 under macOS 12.6)
* [Python 3](https://www.python.org/) (tested with Python 3.9)

SileroVAD-ELAN is written in Python 3, and also depends on the following
Python packages, all of which should be installed in a virtual environment:

* [Silero-VAD](https://github.com/snakers4/silero-vad), installed with all
   of its dependencies. This can be done with `pip` and a clone of the
   current Silero-VAD GitHub repository.
* soundfile (for Windows 10 only)

Under Windows 10, the following commands can be used to fetch and install the
necessary Python packages:
```
git clone https://github.com/l12maro/SileroVAD-Elan
cd SileroVAD-Elan

python3 -m virtualenv venv-silerovad
source ./venv-silerovad/Scripts/activate

git clone https://github.com/snakers4/silero-vad.git
pip install silero
pip install -q torchaudio
```
  
Once all of these tools and packages have been installed, SileroVAD-Elan can
be made available to ELAN as follows:

1. Edit the file `SileroVAD-elan.sh` to specify a Unicode-friendly language and
   locale (if `en_US.UTF-8` isn't available on your computer).
2. To make SileroVAD-ELAN available to ELAN, move your SileroVAD-ELAN directory
   into ELAN's `extensions` directory.  This directory is found in different
   places under different operating systems:
   
   * Under macOS, right-click on `ELAN_6.4` in your `/Applications`
     folder and select "Show Package Contents", then copy your `SileroVAD-ELAN`
     folder into `ELAN_6.4.app/Contents/app/extensions`.
   * Under Linux, copy your `SileroVAD-ELAN` folder into `ELAN_6-4/app/extensions`.
   * Under Windows, copy your `SileroVAD-ELAN` folder into `C:\Users\AppData\Local\ELAN_6-4\app\extensions`.

Once ELAN is restarted, it will now include 'Silero voice activity detection'
in the list of Recognizers found under the 'Recognizer' tab in Annotation Mode.
The user interface for this recognizer allows users to enter the settings needed
to apply voice activity detection to a selected WAV audio recording that hasx
been linked to this ELAN transcript.  Additional settings (e.g., the speech vs.
non-speech threshold, constant adjustments to the start and end-times of 
recognized speech segments, etc.) can be configured through the recognizer
interface, as well.

Once these settings have been entered in SileroVAD-ELAN, pressing the `Start`
button will begin applying Voxseg's voice activity detection to the selected
audio recording.  Once that process is complete, if no errors occurred, ELAN
will allow the user to load the resulting tier with the automatically
recognized speech segments into the current transcript.

## Limitations

This is an alpha release of Silero-VAD-ELAN, and has only been tested under Windows
(10) with Python 3.9.

