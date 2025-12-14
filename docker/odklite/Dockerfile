FROM ubuntu:24.04
LABEL maintainer="obo-tools@googlegroups.com"

ENV ROBOT_VERSION=1.9.8
ENV DOSDP_VERSION=0.19.3
ENV RELATION_GRAPH=2.3.3
ENV DICER_VERSION=0.2.1
ENV ODK_ROBOT_PLUGIN_VERSION=0.2.0
ENV SSSOM_JAVA_VERSION=1.5.1

WORKDIR /odk
ENV JAVA_HOME="/usr"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/odk/bin:$PATH"

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
        sqlite3 \
        gh

# Install Python environment (copied over from the builder image).
COPY --from=obolibrary/odkbuild:latest /staging/lite /

# Create base directories
RUN mkdir -p /odk/tools /odk/resources/robot/plugins /odk/bin

# Install ROBOT.
RUN wget -nv $ROBOT_JAR \
        -O /odk/tools/robot.jar && \
    echo "#!/bin/sh" > /odk/bin/robot && \
    echo "exec java \$ROBOT_JAVA_ARGS -jar /odk/tools/robot.jar \"\$@\"" >> /odk/bin/robot && \
    chmod 755 /odk/bin/robot && \
    wget -nv https://raw.githubusercontent.com/ontodev/robot/v$ROBOT_VERSION/robot-core/src/main/resources/report_profile.txt \
        -O /odk/resources/robot/profile.txt

# Install DOSDPTOOLS.
RUN wget -nv https://github.com/INCATools/dosdp-tools/releases/download/v$DOSDP_VERSION/dosdp-tools-$DOSDP_VERSION.tgz && \
    tar zxf dosdp-tools-$DOSDP_VERSION.tgz && \
    rm dosdp-tools-$DOSDP_VERSION.tgz && \
    mv dosdp-tools-$DOSDP_VERSION /odk/tools/dosdptools && \
    ln -s /odk/tools/dosdptools/bin/dosdp-tools /odk/bin/dosdp-tools && \
    wget -nv --no-check-certificate https://raw.githubusercontent.com/INCATools/dead_simple_owl_design_patterns/master/src/simple_pattern_tester.py \
        -O /odk/bin/simple_pattern_tester.py && \
    chmod 755 /odk/bin/simple_pattern_tester.py

# Install ODK plugin for ROBOT
RUN wget -nv -O /odk/resources/robot/plugins/odk.jar https://github.com/INCATools/odk-robot-plugin/releases/download/odk-robot-plugin-$ODK_ROBOT_PLUGIN_VERSION/odk.jar

# Install SSSOM-Java (CLI tool & ROBOT plugin)
RUN wget -nv -O /odk/resources/robot/plugins/sssom.jar https://github.com/gouttegd/sssom-java/releases/download/sssom-java-$SSSOM_JAVA_VERSION/sssom-robot-plugin-$SSSOM_JAVA_VERSION.jar && \
    wget -nv -O /odk/bin/sssom-cli https://github.com/gouttegd/sssom-java/releases/download/sssom-java-$SSSOM_JAVA_VERSION/sssom-cli && \
    chmod +x /odk/bin/sssom-cli

# Install relation-graph
RUN wget -nv https://github.com/balhoff/relation-graph/releases/download/v$RELATION_GRAPH/relation-graph-cli-$RELATION_GRAPH.tgz && \
    tar -zxvf relation-graph-cli-$RELATION_GRAPH.tgz && \
    rm relation-graph-cli-$RELATION_GRAPH.tgz && \
    mv relation-graph-cli-$RELATION_GRAPH /odk/tools/relation-graph && \
    ln -s /odk/tools/relation-graph/bin/relation-graph /odk/bin/relation-graph

# Install the Dicer CLI tool
RUN wget -nv https://github.com/gouttegd/dicer/releases/download/dicer-$DICER_VERSION/dicer-cli \
        -O /odk/bin/dicer-cli && \
    chmod +x /odk/bin/dicer-cli

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
COPY --chmod=755 scripts/odk-info.sh /odk/bin/odk-info
RUN sed -i s/@@ODK_IMAGE_VERSION@@/$ODK_VERSION/ /odk/bin/odk-info

# Install a helper script to launch a repository update
COPY --chmod=755 scripts/update_repo.sh /odk/bin/update_repo

# Install the OBO extended prefix map
COPY resources/obo.epm.json /odk/resources

# Install anything that may be missing from ODK-Core
RUN odk install /odk

# Run the ODK-Core by default
CMD odk
