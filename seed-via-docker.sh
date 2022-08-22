#!/bin/sh

set -e

ODK_IMAGE=${ODK_IMAGE:-odkfull}
ODK_TAG=${ODK_TAG:-latest}

docker run -v $HOME/.gitconfig:/root/.gitconfig -v $PWD:/work -w /work --rm obolibrary/$ODK_IMAGE:$ODK_TAG /tools/odk.py seed "$@"
