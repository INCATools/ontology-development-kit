#!/bin/bash

IMAGE=${IMAGE:-odkfull}

program_name=$1; shift
echo -n "Checking for $program_name... "
docker run --rm -ti obolibrary/$IMAGE $@ >/dev/null && echo OK || echo KO
