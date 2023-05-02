::!/bin/bash
::
:: Set a number of environmental variables and locale-related settings needed
:: for this recognizer to run as expected before calling the recognizer itself.
::
:: It seems that recognizer processes invoked by ELAN don't inherit any regular
:: environmental variables (like PATH), which makes it difficult to track down
:: where both Python and ffmpeg(1) might be.  These same processes also have
:: their locale set to C.  This implies a default ASCII file encoding, which
:: causes some scripts to refuse to run (since many assume a more Unicode-
:: friendly view of the world somewhere in their code).

:: **
:: ** Edit the following line to point to the directory in which 'ffmpeg' is
:: ** found on this computer.
:: **
SET FFMPEG_DIR=""

SET LC_ALL="en_US.UTF-8"
SET PYTHONIOENCODING="utf-8"
SET PATH="%PATH%:%FFMPEG_DIR%"


:: execute the app
".\venv\Scripts\python.exe" "sileroVAD-elan.py" runserver

:: Activate the virtual environment, then execute the main script.
::".\venv\Scripts\python" "sileroVAD-elan.py" runserver