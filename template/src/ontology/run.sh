#!/bin/sh
docker run -v $PWD/../../:/work -w /work/src/ontology --rm -ti obolibrary/osklite "$@"
