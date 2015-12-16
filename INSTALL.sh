#!/bin/sh
test -d bin || mkdir -p bin
wget http://build.berkeleybop.org/userContent/owltools/owltools -O bin/owltools
wget http://build.berkeleybop.org/userContent/owltools/ontology-release-runner -O bin/ontology-release-runner
wget http://build.berkeleybop.org/userContent/owltools/owltools-runner-all.jar -O bin/owltools-runner-all.jar
wget http://build.berkeleybop.org/userContent/owltools/owltools-oort-all.jar -O bin/owltools-oort-all.jar
wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot -O bin/robot
wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot.jar -O bin/robot.jar
chmod +x bin/*
echo "now type:"
echo export PATH=\$PATH:$PWD/bin
