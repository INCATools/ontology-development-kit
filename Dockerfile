# Final ODK image
# (built upon the odklite image)
ARG ODKLITE_TAG=latest
FROM obolibrary/odklite:${ODKLITE_TAG}
LABEL maintainer="obo-tools@googlegroups.com"

WORKDIR /odk

ARG ODK_VERSION 0.0.0
ENV ODK_VERSION=$ODK_VERSION

# Software versions
# Jena 5.x requires Java 17, so for now we are stuck with Jena 4.x
ENV JENA_VERSION=4.9.0
ENV KGCL_JAVA_VERSION=0.5.1
ENV SCALA_CLI_VERSION=1.8.0
ENV OWLTOOLS_VERSION=2020-04-06
ENV YQ_VERSION=4.50.1

# Avoid repeated downloads of script dependencies by mounting the local coursier cache:
# docker run -v $HOME/.coursier/cache/v1:/odk/tools/.coursier-cache ...
ENV COURSIER_CACHE="/odk/tools/.coursier-cache"

# Install tools provided by Ubuntu.
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends  \
    build-essential \
    openssh-client \
    openjdk-11-jdk-headless \
    maven \
    python3-dev \
    subversion \
    automake \
    aha \
    dos2unix \
    libjson-perl \
    libbusiness-isbn-perl \
    pkg-config \
    xlsx2csv \
    nodejs \
    npm \
    graphviz \
    python3-psycopg2 \
    libpcre3

# Install run-time dependencies for Soufflé.
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        g++ \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        mcpp \
        zlib1g-dev

# Copy everything that we have prepared in the builder image.
COPY --from=obolibrary/odkbuild:latest /staging/full /

# Install Konclude.
# On x86_64, we get it from a pre-built release from upstream; on arm64,
# we use a custom pre-built binary to which we just need to add the
# run-time dependencies (the binary is not statically linked).
ARG TARGETARCH
RUN test "x$TARGETARCH" = xamd64 && ( \
        wget -nv https://github.com/konclude/Konclude/releases/download/v0.7.0-1138/Konclude-v0.7.0-1138-Linux-x64-GCC-Static-Qt5.12.10.zip \
            -O /odk/Konclude.zip && \
        unzip Konclude.zip && \
        mv Konclude-v0.7.0-1138-Linux-x64-GCC-Static-Qt5.12.10/Binaries/Konclude /odk/bin/Konclude && \
        rm -rf Konclude-v0.7.0-1138-Linux-x64-GCC-Static-Qt5.12.10 && \
        rm Konclude.zip \
    ) || ( \
        DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
            libqt5xml5 libqt5network5 libqt5concurrent5 && \
        wget -nv https://incenp.org/files/softs/konclude/0.7/Konclude-v0.7.0-1138-Linux-arm64-GCC.zip \
            -O /odk/Konclude.zip && \
        unzip Konclude.zip && \
        mv Konclude-v0.7.0-1138-Linux-arm64-GCC/Binaries/Konclude /odk/bin/Konclude && \
        rm -rf Konclude-v0.7.0-1138-Linux-arm64-GCC && \
        rm Konclude.zip \
    )

# Install OWLTOOLS.
RUN wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools \
        -O /odk/bin/owltools && \
    wget -nv https://github.com/owlcollab/owltools/releases/download/$OWLTOOLS_VERSION/owltools-oort-all.jar \
        -O /odk/tools/owltools-oort-all.jar && \
    echo "#!/bin/sh" > /odk/bin/ontology-release-runner && \
    echo "exec java -jar /odk/tools/owltools-oort-all.jar \"\$@\"" >> /odk/bin/ontology-release-runner && \
    chmod +x /odk/bin/owltools && \
    chmod +x /odk/bin/ontology-release-runner

# Install Jena.
RUN wget -nv http://archive.apache.org/dist/jena/binaries/apache-jena-$JENA_VERSION.tar.gz -O- | tar xzC /odk/tools && \
    mv /odk/tools/apache-jena-$JENA_VERSION /odk/tools/apache-jena && \
    find /odk/tools/apache-jena/bin -type f -executable -exec ln -s {} /odk/bin \;

# Install Scala-CLI
RUN wget -nv https://github.com/VirtusLab/scala-cli/releases/download/v$SCALA_CLI_VERSION/scala-cli.jar \
        -O /odk/tools/scala-cli.jar && \
    echo "#!/bin/sh" > /odk/bin/scala-cli && \
    echo "exec java -jar /odk/tools/scala-cli.jar \"\$@\"" >> /odk/bin/scala-cli && \
    chmod 0755 /odk/bin/scala-cli

# Install obographviz
RUN npm install -g obographviz && \
    chown -R root:root /usr/local/lib/node_modules

# Install KGCL ROBOT plugin
RUN wget -nv -O /odk/resources/robot/plugins/kgcl.jar https://github.com/gouttegd/kgcl-java/releases/download/kgcl-java-$KGCL_JAVA_VERSION/kgcl-robot-plugin-$KGCL_JAVA_VERSION.jar

# Install Mike Farah's (mf) YQ command-line YAML, JSON and XML processor
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        wget -nv https://github.com/mikefarah/yq/releases/download/v$YQ_VERSION/yq_linux_amd64 -O /odk/bin/yq-mf && \
        chmod 0755 /odk/bin/yq-mf ; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        wget -nv https://github.com/mikefarah/yq/releases/download/v$YQ_VERSION/yq_linux_arm64 -O /odk/bin/yq-mf && \
        chmod 0755 /odk/bin/yq-mf ; \
    else \
        echo "Unsupported TARGETARCH: $TARGETARCH" && exit 1 ; \
    fi

