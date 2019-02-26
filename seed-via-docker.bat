::BATCH file to seed new ontology repo via docker
docker run -v %userprofile%/.gitconfig:/root/.gitconfig -v %cd%:/work -w /work --rm -ti obolibrary/odkfull /tools/odk.py seed %*