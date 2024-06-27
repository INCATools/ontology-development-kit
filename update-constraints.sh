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
python3 -m pip freeze > constraints.txt

test -n "$(head constraints.txt)"
