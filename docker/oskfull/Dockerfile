FROM openjdk:8
MAINTAINER Chris Mungall <cjmungall@lbl.gov>

##RUN apt-get -y update && apt-get install -y software-properties-common python-software-properties
RUN apt-get install -y curl

# Install Maven.
##RUN apt-get -y update && apt-get install -y maven

# Install Git.
RUN apt-get -y update && apt-get install -y git

WORKDIR /tools

ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
RUN wget http://build.berkeleybop.org/userContent/owltools/owltools -O /tools/owltools
RUN wget http://build.berkeleybop.org/userContent/owltools/ontology-release-runner -O /tools/ontology-release-runner
RUN wget http://build.berkeleybop.org/userContent/owltools/owltools-oort-all.jar -O /tools/owltools-oort-all.jar
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot -O /tools/robot
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot.jar -O /tools/robot.jar
RUN chmod +x /tools/*
ENV PATH "/tools/:$PATH"

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -q -y \
  python3-pip \
  perl

# Setup dosdp tools
ENV V=0.9
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$V/dosdp-tools-$V.tgz
RUN tar -zxvf dosdp-tools-$V.tgz && mv dosdp-tools-$V /tools/dosdp-tools
ENV PATH "/tools/dosdp-tools/bin:$PATH"

# Python
RUN pip3 install jsonschema ruamel.yaml requests jsonpath_rw
RUN wget --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py -O /tools/simple_pattern_tester.py && chmod +x /tools/*


CMD make -h
