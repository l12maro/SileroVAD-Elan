::!/bin/bash
::
:: Set a number of environmental variables and locale-related settings needed
:: for this recognizer to run as expected before calling the recognizer itself.
::
:: It seems that recognizer processes invoked by ELAN don't inherit any regular
:: environmental variables (like PATH).  This implies a default ASCII file encoding, which
:: causes some scripts to refuse to run (since many assume a more Unicode-
:: friendly view of the world somewhere in their code).

SET LC_ALL="en_US.UTF-8"
SET PYTHONIOENCODING="utf-8"


:: execute the app
".\venv\Scripts\python.exe" "sileroVAD-elan.py" runserver

:: Activate the virtual environment, then execute the main script.
<<<<<<< HEAD
::".\venv\Scripts\python" "sileroVAD-elan.py" runserver
=======
".\venv-silerovad\Scripts\python" ".\sileroVAD-elan.py" runserver
>>>>>>> bc11bebe3d2d5d09cfae2d86fa0a43619192d296
