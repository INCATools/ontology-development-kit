#!/bin/sh

set -e

IMAGE=${IMAGE:-odkfull}

docker run -v $HOME/.gitconfig:/root/.gitconfig -v $PWD:/work -w /work --rm obolibrary/$IMAGE /tools/odk.py seed "$@"
