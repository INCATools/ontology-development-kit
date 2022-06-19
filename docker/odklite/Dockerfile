FROM ubuntu:22.04
LABEL maintainer="obo-tools@googlegroups.com"

ENV ROBOT_VERSION=1.9.0
ENV DOSDP_VERSION=0.19.3
ENV OWLTOOLS_VERSION=2020-04-06
ENV AMMONITE_VERSION=2.0.3

WORKDIR /tools
ENV JAVA_HOME="/usr"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/tools:/tools/dosdp-tools/bin:$PATH"

ARG ODK_VERSION=0.0.0
ENV ODK_VERSION=$ODK_VERSION

ARG ROBOT_JAR=https://github.com/ontodev/robot/releases/download/v$ROBOT_VERSION/robot.jar
ENV ROBOT_JAR=$ROBOT_JAR

# Install base tools from Ubuntu.
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        git \
        openjdk-11-jre-headless \
        python3-pip \
        python-is-python3 \
        make \
        unzip \
        wget \
        curl \
        jq \
        rsync \
        time

# Install Python environment (copied over from the builder image).
COPY --from=obolibrary/odkbuild:latest /staging/lite /

# Install ROBOT.
RUN wget -nv $ROBOT_JAR \
        -O /tools/robot.jar && \
    wget -nv https://raw.githubusercontent.com/ontodev/robot/v$ROBOT_VERSION/bin/robot \
        -O /tools/robot && \
    chmod 755 /tools/robot

# Install DOSDPTOOLS.
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$DOSDP_VERSION/dosdp-tools-$DOSDP_VERSION.tgz && \
    tar zxf dosdp-tools-$DOSDP_VERSION.tgz && \
    rm dosdp-tools-$DOSDP_VERSION.tgz && \
    mv dosdp-tools-$DOSDP_VERSION /tools/dosdp-tools && \
    wget -nv --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py \
        -O /tools/simple_pattern_tester.py && \
    chmod 755 /tools/simple_pattern_tester.py

# Install OWLTOOLS.
RUN wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools \
        -O /tools/owltools && \
    wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/ontology-release-runner \
        -O /tools/ontology-release-runner && \
    wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools-oort-all.jar \
        -O /tools/owltools-oort-all.jar && \
    chmod +x /tools/owltools && \
    chmod +x /tools/ontology-release-runner && \
    chmod +x /tools/owltools-oort-all.jar

# Install Ammonite.
RUN wget -nv https://github.com/lihaoyi/Ammonite/releases/download/$AMMONITE_VERSION/2.13-$AMMONITE_VERSION \
        -O /tools/amm && \
    chmod 755 /tools/amm && \
    /tools/amm /dev/null

# Install the ODK itself.
COPY odk/make-release-assets.py /tools
COPY odk/odk.py /tools
COPY template/ /tools/templates/
RUN chmod 755 /tools/*.py
CMD python3 /tools/odk.py
