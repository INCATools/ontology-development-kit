#!/bin/bash
# Wrapper script for ODK.
#
# This script maps the current directory (pwd) into the container at /work
# If you want to simply enter the container and take a look around try:
# sh odk.sh bash
# You should now find your self inside the running container. try ls to see wether
# You can still see the files in your current directory, and then robot --version to see wether
# the command line works. You can leave the container with the "exit" command
# Alternatively you can directly run robot from your own machine like this:
# sh odk.sh robot --version
# Lastly: the script will read your local ROBOT_JAVA_ARGS variable for
# Java options.. Default is "-Xmx8G"

if [[ -z "${ROBOT_JAVA_ARGS}" ]]; then
  MEMORY="-Xmx8G"
else
  MEMORY="${ROBOT_JAVA_ARGS}"
fi

echo "Running ODK with ${MEMORY} (Maximum Java Memory)" >&2
docker run -e ROBOT_JAVA_ARGS="${MEMORY}" -e JAVA_OPTS="${MEMORY}" -v $PWD/:/work -w /work --rm -ti obolibrary/odkfull "$@"
