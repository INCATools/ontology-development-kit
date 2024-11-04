#!/bin/sh

set -e

if [ "x$1" = x--install-virtualenv ]; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-virtualenv
fi

virtualenv tmpdir
. tmpdir/bin/activate
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt.full

# For some context of this see here: 
# https://github.com/INCATools/ontology-development-kit/commit/f1bdb983e2ae0128e7a8fbfb60b7c05755c4c5d0
python3 -m pip freeze | grep -v "setuptools" > constraints.txt

test -n "$(head constraints.txt)"
