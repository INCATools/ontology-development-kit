#!/bin/bash

ODK_IMAGE=${ODK_IMAGE:-odkfull}
ODK_TAG=${ODK_TAG:-latest}

program_name=$1; shift
echo -n "Checking for $program_name... "
docker run --rm obolibrary/$ODK_IMAGE:$ODK_TAG $@ >/dev/null && echo OK || echo KO
