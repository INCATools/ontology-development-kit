#!/bin/sh

set -e

virtualenv tmpdir
. tmpdir/bin/activate
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt.full
python3 -m pip freeze > constraints.txt
