#!/bin/sh
docker run -v $PWD:/work -w /work --rm -ti obolibrary/oskfull ./seed-my-ontology-repo.pl -e obo-ci-reports-all@groups.io "$@"
