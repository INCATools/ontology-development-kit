FROM openjdk:8

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
ENV V=0.10.1
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$V/dosdp-tools-$V.tgz
RUN tar -zxvf dosdp-tools-$V.tgz && mv dosdp-tools-$V /tools/dosdp-tools
ENV PATH "/tools/dosdp-tools/bin:$PATH"

WORKDIR /opt/starter-kit
ADD . /opt/starter-kit/
RUN chmod +x ./seed-my-ontology-repo.pl

CMD ./seed-my-ontology-repo.pl --help
