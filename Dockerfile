### From https://stackoverflow.com/questions/51121875/how-to-run-docker-with-python-and-java
### 1. Get Linux
FROM ubuntu:18.04
LABEL maintainer="obo-tools@googlegroups.com" 

### 2. Get Java, Python and all required system libraries (version control etc)
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"
#ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:swi-prolog/stable && apt-get upgrade -y \
 && apt-get install -y software-properties-common \
  build-essential git \
  openjdk-8-jre openjdk-8-jdk swi-prolog


### 3. Python and all required system libraries (version control etc)

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev subversion make automake gcc g++ unzip rsync curl wget jq openssl git xlsx2csv \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip setuptools \
	&& if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
	&& if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
	&& rm -r /root/.cache

### 4. Install custom tools

###### Python libraries ######
WORKDIR /tools
ENV PATH "/tools/:$PATH"
COPY requirements.txt /tools/
RUN pip3 install -r requirements.txt

###### owltools & OORT ######
# For now we get these from jenkins builds, but these should be obtained
# by composing existing Dockerfiles, or by obtaining directly from maven
ENV OWLTOOLS 2020-04-06
RUN wget https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/owltools -O /tools/owltools && \
    wget https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/ontology-release-runner -O /tools/ontology-release-runner && \
    wget https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS/owltools-oort-all.jar -O /tools/owltools-oort-all.jar && \
    chmod +x /tools/owltools && \
    chmod +x /tools/ontology-release-runner && \
    chmod +x /tools/owltools-oort-all.jar

###### Konclude, the DL reasoner ######
RUN wget https://github.com/konclude/Konclude/releases/download/v0.6.2-845/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13.zip -O /tools/konclude.zip && \
    unzip /tools/konclude.zip && \
    mv /tools/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13 /tools/konclude_reasoner && \ 
    rm /tools/konclude.zip && \
    chmod +x /tools/konclude_reasoner/Binaries && \
    echo "#!/bin/bash" > /tools/Konclude && \
    echo '/tools/konclude_reasoner/Binaries/Konclude $*' >> /tools/Konclude && \
    chmod +x /tools/Konclude

###### ROBOT ######
ENV ROBOT v1.7.1
ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/$ROBOT/robot.jar
ENV ROBOT_JAR ${ROBOT_JAR}
RUN pwd
RUN wget $ROBOT_JAR -O /tools/robot.jar && \
    wget https://raw.githubusercontent.com/ontodev/robot/$ROBOT/bin/robot -O /tools/robot && \
    chmod +x /tools/robot && \
    chmod +x /tools/robot.jar

# Avoid repeated downloads of script dependencies by mounting the local coursier cache:
# docker run -v $HOME/.coursier/cache/v1:/tools/.coursier-cache ...
ENV COURSIER_CACHE "/tools/.coursier-cache"

###### FASTOBO ######
ENV FASTOBO_VALIDATOR v0.3.0
RUN wget https://dl.bintray.com/fastobo/fastobo-validator/$FASTOBO_VALIDATOR/fastobo_validator-x86_64-linux-musl.tar.gz -O- | tar xzC /tools \
&& chmod +x /tools/fastobo-validator

##### Ammonite #####
RUN (echo "#!/usr/bin/env sh" \
&& curl -L https://github.com/lihaoyi/Ammonite/releases/download/2.0.3/2.13-2.0.3) >/tools/amm \
&& chmod +x /tools/amm
# Force precompile of ammonite files
RUN amm /dev/null

###### DOSDPTOOLS ######
ENV DOSDPVERSION=0.14
ENV PATH "/tools/dosdp-tools/bin:$PATH"
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$DOSDPVERSION/dosdp-tools-$DOSDPVERSION.tgz \
&& tar -zxvf dosdp-tools-$DOSDPVERSION.tgz \
&& mv dosdp-tools-$DOSDPVERSION /tools/dosdp-tools \
&& wget --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py -O /tools/simple_pattern_tester.py \
&& chmod +x /tools/dosdp-tools \
&& chmod +x /tools/simple_pattern_tester.py

###### SPARQLProg ######
# See https://github.com/cmungall/sparqlprog/blob/master/INSTALL.md
RUN swipl -g "Opts=[interactive(false)],pack_install(dcgutils,Opts),pack_install(obo_metadata,Opts),pack_install(index_util,Opts),pack_install(regex,Opts),pack_install(typedef,Opts),halt"
RUN swipl -g "pack_install(sparqlprog, [interactive(false)])" -g halt
#RUN swipl -p library=prolog -l tests/tests.pl -g run_tests,halt
ENV PATH "/root/.local/share/swi-prolog/pack/sparqlprog/bin:$PATH"
RUN ln -sf /root/.local/share/swi-prolog/pack/sparqlprog /tools/

COPY scripts/obo-dash.sh /tools/obodash
RUN cd /tools/ && chmod +x /tools/obodash && git clone https://github.com/OBOFoundry/OBO-Dashboard.git && \
    cd OBO-Dashboard && git checkout docker-dash && echo "DOCKER DASH BRANCH CHECKED OUT" &&\
    python3 -m pip install -r requirements.txt && echo " " >> Makefile &&\
    echo "build/robot.jar:" >> Makefile &&\
    echo "	echo 'skipped ROBOT jar download' && touch \$@" >> Makefile && echo "" >> Makefile

### 5. Install ODK
ARG ODK_VERSION=0.0.0
ENV ODK_VERSION=${ODK_VERSION}


COPY template/ /tools/templates/
COPY odk/ /tools/ 
RUN chmod +x /tools/*.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD python /tools/odk.py
