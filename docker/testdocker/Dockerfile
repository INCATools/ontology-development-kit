# Container to test layer size
FROM ubuntu:18.04
LABEL maintainer="obo-tools@googlegroups.com" 

ENV ROBOT v1.5.0
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR ${ROBOT_JAR}

RUN apt-get update \
  && apt-get install -y curl wget

WORKDIR /tools
ENV PATH "/tools/:$PATH"

RUN wget $ROBOT_JAR -O /tools/robot.jar && \
    wget https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -O /tools/robot && \
    chmod +x /tools/*