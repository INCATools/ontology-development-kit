#!/bin/sh
# Wrapper script for running ROBOT from anywhere
docker run -v $PWD:/work -w /work -e ROBOT_JAVA_ARGS='-Xmx2G' --rm -ti obolibrary/robot "$@"