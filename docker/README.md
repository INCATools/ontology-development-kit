# Dockerfiles for obolibrary/odk{build,lite}

The ODK provides several Docker images. The "main" image is `odkfull`,
whose Dockerfile is in the top-level folder. Instructions on how to
build the full ODK can be found [in the top-level
Makefile](https://github.com/INCATools/ontology-development-kit/blob/master/Makefile).

This folder contains Dockerfiles for building the other images:
`odklite`, `odkbuild`, and `robot`.

The `odklite` image is a lighter variant of `odkfull`, containing a
small subset of the programs and Python modules found in the full ODK.
It is automatically built when building the main `odkfull` image, but it
can also be built separately by using the [corresponding
Makefile](https://github.com/INCATools/ontology-development-kit/blob/master/docker/odklite/Makefile).

The `odkbuild` image is a build artifact solely used as a staging area
to build the `odklite` and `odkfull` images. It is not indended for any
other use.

The `robot` image is a minimalist image containing only _ROBOT_. It is
built separately from the other images using [its own
Makefile](https://github.com/INCATools/ontology-development-kit/blob/master/docker/robot/Makefile).
