FROM ubuntu:24.04
LABEL maintainer="obo-tools@googlegroups.com"

ENV ROBOT_VERSION=1.9.7
ENV DOSDP_VERSION=0.19.3
ENV OWLTOOLS_VERSION=2020-04-06
ENV AMMONITE_VERSION=2.5.9
ENV RELATION_GRAPH=2.3.2

WORKDIR /tools
ENV JAVA_HOME="/usr"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/tools:/tools/dosdptools/bin:/tools/relation-graph/bin:$PATH"

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
        python3-six \
        make \
        unzip \
        wget \
        curl \
        jq \
        rsync \
        time \
        sudo \
        sqlite3

# Install Python environment (copied over from the builder image).
COPY --from=obolibrary/odkbuild:latest /staging/lite /

# Install ROBOT.
RUN wget -nv $ROBOT_JAR \
        -O /tools/robot.jar && \
    wget -nv https://raw.githubusercontent.com/ontodev/robot/v$ROBOT_VERSION/bin/robot \
        -O /tools/robot && \
    chmod 755 /tools/robot &&\
    wget -nv https://raw.githubusercontent.com/ontodev/robot/v$ROBOT_VERSION/robot-core/src/main/resources/report_profile.txt \
        -O /tools/robot_report_profile.txt

# Install DOSDPTOOLS.
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$DOSDP_VERSION/dosdp-tools-$DOSDP_VERSION.tgz && \
    tar zxf dosdp-tools-$DOSDP_VERSION.tgz && \
    rm dosdp-tools-$DOSDP_VERSION.tgz && \
    mv dosdp-tools-$DOSDP_VERSION /tools/dosdptools && \
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
    java -cp /tools/amm ammonite.AmmoniteMain /dev/null

# Install relation-graph
RUN wget -nv https://github.com/balhoff/relation-graph/releases/download/v$RELATION_GRAPH/relation-graph-cli-$RELATION_GRAPH.tgz && \
    tar -zxvf relation-graph-cli-$RELATION_GRAPH.tgz && \
    mv relation-graph-cli-$RELATION_GRAPH /tools/relation-graph && \
    chmod +x /tools/relation-graph

# Install RDF/XML validation script
COPY --chmod=755 scripts/check-rdfxml.sh /tools/check-rdfxml

# Install script to convert JSON context prefix map to CSV prefix map
COPY --chmod=755 scripts/context2csv.py /tools/context2csv

# Make sure we run under an existing user account with UID/GID
# matching the UID/GID of the calling user
COPY --chmod=755 scripts/entrypoint.sh /usr/local/sbin/odkuser-entrypoint.sh
ENTRYPOINT ["/usr/local/sbin/odkuser-entrypoint.sh"]

# Misc tweaks:
# - disable secure_path (we want to be able to use sudo with our custom PATH)
# - remove default user account (we create our own)
# - force Git to accept working on a repository owned by someone else
RUN sed -i '/secure_path/d' /etc/sudoers && \
    userdel -r ubuntu && \
    echo "[safe]\n    directory = *" >> /etc/gitconfig

# Install a script that provides information about the ODK and its tools
COPY --chmod=755 scripts/odk-info.sh /tools/odk-info
RUN sed -i s/@@ODK_IMAGE_VERSION@@/$ODK_VERSION/ /tools/odk-info

# Install the ODK itself.
COPY --chmod=755 odk/make-release-assets.py odk/odk.py /tools
COPY template/ /tools/templates/
CMD python3 /tools/odk.py
