#!/bin/sh

set -e

make IM=obotools/odkfull_m1 IMLITE=obotools/odklite_m1 DEV=obotools/odkdev_m1 ROB=obotools/robot_m1 docker-test
make IM=obotools/odkfull_m1 IMLITE=obotools/odklite_m1 DEV=obotools/odkdev_m1 ROB=obotools/robot_m1 docker-publish
