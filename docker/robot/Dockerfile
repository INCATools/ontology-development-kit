FROM ubuntu:24.04
LABEL maintainer="obo-tools@googlegroups.com" 

WORKDIR /tools

ENV ROBOT=v1.9.7
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR=${ROBOT_JAR}

RUN apt-get update &&\
  apt-get upgrade -y &&\
  apt-get install -y --no-install-recommends make \
    openjdk-11-jre-headless \
    unzip \
    rsync \
    curl

RUN curl -L $ROBOT_JAR -o /tools/robot.jar &&\
    curl -L https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -o /tools/robot && \
    chmod +x /tools/robot && \
    chmod +x /tools/robot.jar
  
ENV PATH="/tools/:$PATH"
RUN echo "Keep me in sync with obolibrary/odkfull!"
CMD robot -h
