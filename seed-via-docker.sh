#!/bin/sh
docker run -v $PWD:/work -w /work --rm -ti obolibrary/odkfull ./odk/odk.py "$@"
