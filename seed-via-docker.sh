#!/bin/sh

set -e

ODK_IMAGE=${ODK_IMAGE:-odkfull}
ODK_TAG=${ODK_TAG:-latest}
ODK_GITNAME=${ODK_GITNAME:-$(git config --get user.name)}
ODK_GITEMAIL=${ODK_GITEMAIL:-$(git config --get user.email)}

docker run -u $(id -u):$(id -g) -v $PWD:/work -w /work --rm obolibrary/$ODK_IMAGE:$ODK_TAG /tools/odk.py seed --gitname "$ODK_GITNAME" --gitemail "$ODK_GITEMAIL" "$@"
