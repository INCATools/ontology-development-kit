FROM openjdk:8-jdk-alpine

RUN apk add --update make

WORKDIR /tools

# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot -O /tools/robot
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot.jar -O /tools/robot.jar
RUN chmod +x /tools/*
ENV PATH "/tools/:$PATH"

CMD make -h

