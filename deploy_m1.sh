#!/bin/sh

set -e

make IM=obolibrary/odkfull_m1 IMLITE=obolibrary/odklite_m1 DEV=obolibrary/odkdev_m1 ROB=obolibrary/robot_m1 docker-build docker-test
make IM=obolibrary/odkfull_m1 IMLITE=obolibrary/odklite_m1 DEV=obolibrary/odkdev_m1 ROB=obolibrary/robot_m1 docker-publish
