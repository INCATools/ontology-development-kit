::BATCH file to seed new ontology repo via docker
::DO NOT USE THIS UNLESS YOU KNOW WHAT IT DOES. Just for development purposes.
docker run -v /c/Users/nicol/.gitconfig:/root/.gitconfig -v /c/Users/nicol/gitt/ontology-development-kit:/work -w /work --rm -ti obolibrary/odkfull /tools/odk.py seed %*
