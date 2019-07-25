FROM openjdk:8-jre-alpine3.9
MAINTAINER Chris Mungall <cjmungall@lbl.gov>

RUN apk add --no-cache make bash

WORKDIR /tools

ENV ROBOT v1.4.1
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR ${ROBOT_JAR}

RUN wget $ROBOT_JAR -O /tools/robot.jar && \
    wget https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -O /tools/robot && \
    chmod +x /tools/*
  
ENV PATH "/tools/:$PATH"
CMD robot -h
