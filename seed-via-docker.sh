#!/bin/sh

set -e

echo "This script only works with ODK 1.3.2 and later. For ODK 1.3.1 or earlier, use https://raw.githubusercontent.com/INCATools/ontology-development-kit/v1.3.1/seed-via-docker.sh"

ODK_IMAGE=${ODK_IMAGE:-odkfull}
ODK_TAG=${ODK_TAG:-latest}
ODK_GITNAME=${ODK_GITNAME:-$(git config --get user.name)}
ODK_GITEMAIL=${ODK_GITEMAIL:-$(git config --get user.email)}

docker run -v $PWD:/work -w /work --rm obolibrary/$ODK_IMAGE:$ODK_TAG /tools/odk.py seed --gitname "$ODK_GITNAME" --gitemail "$ODK_GITEMAIL" "$@"
