#!/bin/sh
###docker run -v $PWD/../../:/work -w /work/src/ontology --rm -ti foobar "$@"
docker run -v $PWD/../../:/work -w /work/src/ontology --rm -ti cmungall/osk "$@"
