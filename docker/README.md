# Dockerfiles for obolibrary/odk{full,lite}

This folder containers Dockerfiles for building the versions of the ODK.

Currently we only make one: odklite. See odklite folder for details.

The main, most frequently maintained image however is odkfull: Instructions on how to build 
the ODK full can be found [in the Makefile here](https://github.com/INCATools/ontology-development-kit/blob/master/Makefile).

Note that these containers are not intended to be built as part of the
ontology generation process. They are here for obo admins to make and
release the docker images required for odk to work.


