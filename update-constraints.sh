#!/bin/sh

set -e

if [ -d /usr/lib/python3/dist-packages ]; then
    # For any Python package already provided by the system, we must
    # force PIP to use the exact same version as the one installed
    find /usr/lib/python3/dist-packages -type d -name '*-info' | \
        sed -E 's,/usr/lib/python3/dist-packages/(.+)-([^-]+)\.(egg|dist)-info,\1==\2,' \
        > pip-constraints.txt
fi

if [ "x$1" = x--install-virtualenv ]; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-virtualenv
fi

virtualenv tmpdir
. tmpdir/bin/activate
export PIP_CONSTRAINT=$(pwd)/pip-constraints.txt
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt.full
python3 -m pip freeze > constraints.txt

test -n "$(head constraints.txt)"
