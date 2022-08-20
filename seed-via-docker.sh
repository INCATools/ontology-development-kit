#!/bin/sh

set -e

ODK_IMAGE=${ODK_IMAGE:-odkfull}

docker run -v $HOME/.gitconfig:/root/.gitconfig -v $PWD:/work -w /work --rm obolibrary/$ODK_IMAGE /tools/odk.py seed "$@"
