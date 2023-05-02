#!/bin/bash
#
# Set a number of environmental variables and locale-related settings needed
# for this recognizer to run as expected before calling the recognizer itself.
#
# It seems that recognizer processes invoked by ELAN don't inherit any regular
# environmental variables (like PATH). This implies a default ASCII file encoding, which
# causes some scripts to refuse to run (since many assume a more Unicode-
# friendly view of the world somewhere in their code).

export LC_ALL="en_US.UTF-8"
export PYTHONIOENCODING="utf-8"

# Activate the virtual environment, then execute the main script.
source ./venv-silerovad/bin/activate
exec python3 ./sileroVAD-elan.py
