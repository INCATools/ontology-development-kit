FROM ubuntu:20.04
LABEL maintainer="obo-tools@googlegroups.com"

ENV ROBOT_VERSION 1.8.1
ENV DOSDP_VERSION 0.17
ENV OWLTOOLS_VERSION 2020-04-06
ENV AMMONITE_VERSION 2.0.3

WORKDIR /tools
ENV JAVA_HOME "/usr"
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PATH "/tools:/tools/dosdp-tools/bin:$PATH"

# Base tools from Ubuntu
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        git \
        openjdk-8-jre-headless \
        python3-pip \
        make \
        unzip \
        wget \
        jq \
        rsync

# Python environment
COPY constraints.txt /tools/constraints.txt
RUN python3 -m pip install -c /tools/constraints.txt \
        dataclasses \
        dataclasses-jsonschema \
        dataclasses-json \
        jinja2 \
        pyyaml \
        dacite \
        click \
        jsonpath_rw \
        ruamel.yaml \
        PyGithub && \
    if [ ! -e /usr/bin/python ] ; then ln -sf /usr/bin/python3 /usr/bin/python ; fi

# ROBOT
RUN wget -nv https://github.com/ontodev/robot/releases/download/v$ROBOT_VERSION/robot.jar \
        -O /tools/robot.jar && \
    wget -nv https://raw.githubusercontent.com/ontodev/robot/v$ROBOT_VERSION/bin/robot \
        -O /tools/robot && \
    chmod 755 /tools/robot

# DOSDPTOOLS
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$DOSDP_VERSION/dosdp-tools-$DOSDP_VERSION.tgz && \
    tar zxf dosdp-tools-$DOSDP_VERSION.tgz && \
    rm dosdp-tools-$DOSDP_VERSION.tgz && \
    mv dosdp-tools-$DOSDP_VERSION /tools/dosdp-tools && \
    wget -nv --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py \
        -O /tools/simple_pattern_tester.py && \
    chmod 755 /tools/simple_pattern_tester.py

# OWLTOOLS
RUN wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools \
        -O /tools/owltools && \
    wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/ontology-release-runner \
        -O /tools/ontology-release-runner && \
    wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools-oort-all.jar \
        -O /tools/owltools-oort-all.jar && \
    chmod +x /tools/owltools && \
    chmod +x /tools/ontology-release-runner && \
    chmod +x /tools/owltools-oort-all.jar

# AMMONITE
RUN wget -nv https://github.com/lihaoyi/Ammonite/releases/download/$AMMONITE_VERSION/2.13-$AMMONITE_VERSION \
        -O /tools/amm && \
    chmod 755 /tools/amm && \
    /tools/amm /dev/null

# ODK
COPY odk/make-release-assets.py /tools
COPY odk/odk.py /tools
COPY template/ /tools/templates/
RUN chmod 755 /tools/*.py
CMD python /tools/odk.py
