### From https://stackoverflow.com/questions/51121875/how-to-run-docker-with-python-and-java
### 1. Get Linux
FROM ubuntu:18.04

ARG ODK_VERSION=0.0.0
ENV ODK_VERSION ${ODK_VERSION}

### 2. Get Python, PIP

RUN apt-get update && apt-get upgrade -y \
 && apt-get install -y software-properties-common \
  build-essential git \
  openjdk-8-jre openjdk-8-jdk

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev subversion make automake gcc g++ unzip rsync curl wget jq openssl git \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip setuptools \
	&& if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
	&& if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
	&& rm -r /root/.cache

WORKDIR /tools
COPY requirements.txt /tools/

# The following row are required to build and install numpy, which is a prerequisite for pandas
#RUN apk add --no-cache make automake gcc g++ subversion

RUN pip3 install -r requirements.txt && pip3 install jsonschema ruamel.yaml requests jsonpath_rw numpy pandas

### 2. Get Java via the package manager

#RUN apk update \
#&& apk add --no-cache bash \
#&& apk add --no-cache --virtual=build-dependencies unzip \
#&& apk add --no-cache curl \
#&& apk add --no-cache rsync

#&& apk upgrade \

#ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"
ENV ROBOT v1.5.0
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR ${ROBOT_JAR}

#RUN apk --no-cache add openssl wget
#RUN apk add --no-cache jq

# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
RUN wget http://build.berkeleybop.org/userContent/owltools/owltools -O /tools/owltools && \
    wget http://build.berkeleybop.org/userContent/owltools/ontology-release-runner -O /tools/ontology-release-runner && \
    wget http://build.berkeleybop.org/userContent/owltools/owltools-oort-all.jar -O /tools/owltools-oort-all.jar 

# Installing Konclude
RUN wget https://github.com/konclude/Konclude/releases/download/v0.6.2-845/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13.zip -O /tools/konclude.zip && \
    unzip /tools/konclude.zip && \
    mv /tools/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13 /tools/konclude_reasoner && \ 
    rm /tools/konclude.zip && \
    chmod +x /tools/konclude_reasoner/Binaries && \
    echo "#!/bin/bash" > /tools/Konclude && \
    echo '/tools/konclude_reasoner/Binaries/Konclude $*' >> /tools/Konclude && \
    chmod +x /tools/Konclude

RUN wget $ROBOT_JAR -O /tools/robot.jar && \
    wget https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -O /tools/robot && \
    chmod +x /tools/*
    
ENV PATH "/tools/:$PATH"

# Setup fastobo-validator
RUN wget https://dl.bintray.com/fastobo/fastobo-validator/stable/fastobo_validator-x86_64-linux-musl.tar.gz -O- | tar xzC /tools

# Setup dosdp tools
ENV V=0.13.1
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$V/dosdp-tools-$V.tgz && tar -zxvf dosdp-tools-$V.tgz && mv dosdp-tools-$V /tools/dosdp-tools
ENV PATH "/tools/dosdp-tools/bin:$PATH"

# dosdp python
RUN wget --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py -O /tools/simple_pattern_tester.py && chmod +x /tools/*


COPY template/ /tools/templates/
COPY odk/ /tools/

CMD python /tools/odk.py
