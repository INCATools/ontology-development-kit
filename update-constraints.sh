#!/bin/sh

set -e

in_docker=0
[ "x$1" = x--in-docker ] && in_docker=1

if [ $in_docker -eq 1 ]; then
    # Install the same base Python packages as the one present in the
    # ODK builder image.
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-dev python3-pip

    # Get the list of the Python packages that were actually installed
    # so we can instruct PIP to use the same versions of said packages.
    find /usr/lib/python3/dist-packages -type d -name '*-info' | \
        sed -E 's,/usr/lib/python3/dist-packages/(.+)-([^-]+)\.(egg|dist)-info,\1==\2,' | \
        sort > pip-constraints.txt

    # Now additionally install virtualenv, which we will need to
    # install all ODK packages in a separate environment.
    apt-get install -y --no-install-recommends python3-virtualenv

    # Make sure we are using below the same version of Python as the
    # one in the ODK
    PYTHON_VERSION=$(python3 --version | sed -E 's,^Python 3\.([0-9]+)\.[0-9]+$,3.\1,')
fi

# The version of Python should match
virtualenv -p ${PYTHON_VERSION:-3.12} tmpdir
. tmpdir/bin/activate
[ -f pip-constraints.txt ] && export PIP_CONSTRAINT=$(pwd)/pip-constraints.txt
python3 -m pip install -r requirements.txt.full
python3 -m pip freeze > constraints.txt

test -n "$(head constraints.txt)"
