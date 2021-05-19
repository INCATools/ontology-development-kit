#!/bin/sh

set -e

docker run -v $HOME/.gitconfig:/root/.gitconfig -v $PWD:/work -w /work --rm obolibrary/odkfull /tools/odk.py seed "$@"
