#!/bin/sh

set -e

docker run -v $HOME/.gitconfig:/root/.gitconfig -v $PWD:/work -w /work --rm -ti obolibrary/odkfull /tools/odk.py seed "$@"
