### From https://stackoverflow.com/questions/51121875/how-to-run-docker-with-python-and-java
### 1. Get Linux
FROM ubuntu:20.04
LABEL maintainer="obo-tools@googlegroups.com" 

### 2. Get Java, Python and all required system libraries (version control etc)
ENV JAVA_HOME="/usr"
WORKDIR /tools
ENV PATH "/tools/:$PATH"
COPY requirements.txt.lite /tools/requirements.txt
COPY odk/make-release-assets.py /tools/

#ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
# LAYERSIZE ~1000MB
RUN apt-get update &&\
  apt-get install -y software-properties-common &&\
  apt-get upgrade -y &&\
  apt-get install -y build-essential \
    git \
    openjdk-8-jre \
    make \
    unzip \
    rsync \
    curl \
    jq \
    openssl

###### owltools & OORT ######
# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
ENV OWLTOOLS 2020-04-06
RUN curl -L https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/owltools -o /tools/owltools && \
    curl -L https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/ontology-release-runner -o /tools/ontology-release-runner && \
    curl -L https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/owltools-oort-all.jar -o /tools/owltools-oort-all.jar && \
    chmod +x /tools/owltools && \
    chmod +x /tools/ontology-release-runner && \
    chmod +x /tools/owltools-oort-all.jar

###### ROBOT ######
ENV ROBOT v1.8.1
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR ${ROBOT_JAR}

# LAYERSIZE ~66MB
RUN curl -L $ROBOT_JAR -o /tools/robot.jar &&\
    curl -L https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -o /tools/robot && \
    chmod +x /tools/robot && \
    chmod +x /tools/robot.jar

### 5. Install ODK
ARG ODK_VERSION=0.0.0
ENV ODK_VERSION=${ODK_VERSION}

### TODO REVIEW THIS. As we speak, jq is official still stalled at 1.5, but for the walk function, we
### Need 1.6 - once 1.6 is offcial, the following RUN can be removed.
# LAYERSIZE: ~4MB
RUN curl -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -o /tools/jq && chmod +x /tools/jq

COPY odk/odk.py /tools/
COPY template/ /tools/templates/
RUN chmod +x /tools/*.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN echo "Keep me in sync with obolibrary/odkfull!"

CMD python /tools/odk.py
