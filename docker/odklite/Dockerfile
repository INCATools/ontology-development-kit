FROM openjdk:8-jdk-alpine
MAINTAINER Chris Mungall <cjmungall@lbl.gov>

RUN apk add --update make

WORKDIR /tools

# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot -O /tools/robot
RUN wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot.jar -O /tools/robot.jar
RUN chmod +x /tools/*
ENV PATH "/tools/:$PATH"

# Setup dosdp tools
ENV V=0.10.1
RUN wget -nv  https://github.com/INCATools/dosdp-tools/releases/download/v$V/dosdp-tools-$V.tgz
RUN tar -zxvf dosdp-tools-$V.tgz && mv dosdp-tools-$V /tools/dosdp-tools
ENV PATH "/tools/dosdp-tools/bin:$PATH"

CMD make -h

