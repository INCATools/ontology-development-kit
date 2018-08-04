#!/bin/sh
docker run -v $PWD:/work -w /work --rm -ti obolibrary/odkfull ./seed-my-ontology-repo.pl -e obo-ci-reports-all@groups.io "$@"
