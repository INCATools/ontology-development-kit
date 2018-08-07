FROM openjdk:8-jdk-alpine
MAINTAINER Chris Mungall <cjmungall@lbl.gov>

RUN apk add --no-cache make bash

WORKDIR /tools

RUN wget https://github.com/ontodev/robot/releases/download/v1.2.0-alpha-1/robot.jar -O /tools/robot.jar && \
    wget https://raw.githubusercontent.com/ontodev/robot/v1.2.0-alpha-1/bin/robot -O /tools/robot && \
    chmod +x /tools/*
    
ENV PATH "/tools/:$PATH"
CMD robot -h
