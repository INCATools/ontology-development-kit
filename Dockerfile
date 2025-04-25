# Final ODK image
# (built upon the odklite image)
ARG ODKLITE_TAG=latest
FROM obolibrary/odklite:${ODKLITE_TAG}
LABEL maintainer="obo-tools@googlegroups.com"

ENV PATH="/tools/apache-jena/bin:/usr/local/share/swi-prolog/pack/sparqlprog/bin:$PATH"

ARG ODK_VERSION 0.0.0
ENV ODK_VERSION=$ODK_VERSION

# Software versions
# Jena 5.x requires Java 17, so for now we are stuck with Jena 4.x
ENV JENA_VERSION=4.9.0
ENV KGCL_JAVA_VERSION=0.5.1
ENV AMMONITE_VERSION=2.5.9
ENV SCALA_CLI_VERSION=1.5.4
ENV OWLTOOLS_VERSION=2020-04-06

# Avoid repeated downloads of script dependencies by mounting the local coursier cache:
# docker run -v $HOME/.coursier/cache/v1:/tools/.coursier-cache ...
ENV COURSIER_CACHE="/tools/.coursier-cache"

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
    gh \
    nodejs \
    npm \
    graphviz \
    python3-psycopg2 \
    swi-prolog \
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
            -O /tools/Konclude.zip && \
        unzip Konclude.zip && \
        mv Konclude-v0.7.0-1138-Linux-x64-GCC-Static-Qt5.12.10/Binaries/Konclude /tools/Konclude && \
        rm -rf Konclude-v0.7.0-1138-Linux-x64-GCC-Static-Qt5.12.10 && \
        rm Konclude.zip \
    ) || ( \
        DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
            libqt5xml5 libqt5network5 libqt5concurrent5 && \
        wget -nv https://incenp.org/files/softs/konclude/0.7/Konclude-v0.7.0-1138-Linux-arm64-GCC.zip \
            -O /tools/Konclude.zip && \
        unzip Konclude.zip && \
        mv Konclude-v0.7.0-1138-Linux-arm64-GCC/Binaries/Konclude /tools/Konclude && \
        rm -rf Konclude-v0.7.0-1138-Linux-arm64-GCC && \
        rm Konclude.zip \
    )

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

# Install Jena.
RUN wget -nv http://archive.apache.org/dist/jena/binaries/apache-jena-$JENA_VERSION.tar.gz -O- | tar xzC /tools && \
    mv /tools/apache-jena-$JENA_VERSION /tools/apache-jena

# Install Ammonite
RUN wget -nv https://github.com/lihaoyi/Ammonite/releases/download/$AMMONITE_VERSION/2.13-$AMMONITE_VERSION \
        -O /tools/amm && \
    chmod 755 /tools/amm && \
    java -cp /tools/amm ammonite.AmmoniteMain /dev/null

# Install Scala-CLI
RUN wget -nv https://github.com/VirtusLab/scala-cli/releases/download/v$SCALA_CLI_VERSION/scala-cli.jar \
        -O /tools/scala-cli.jar && \
    echo "#!/bin/bash" > /tools/scala-cli && \
    echo "java -jar /tools/scala-cli.jar \"\$@\"" >> /tools/scala-cli && \
    chmod 0755 /tools/scala-cli

# Install SPARQLProg.
RUN swipl -g "pack_install(sparqlprog, [interactive(false),global(true)])" -g halt

# Install obographviz
RUN npm install -g obographviz && \
    chown -R root:root /usr/local/lib/node_modules

# Install OBO-Dashboard.
COPY scripts/obodash /tools
RUN chmod +x /tools/obodash && \
    git clone --depth 1 https://github.com/OBOFoundry/OBO-Dashboard.git && \
    cd OBO-Dashboard && \
    python3 -m pip install -r requirements.txt --break-system-packages && \
    echo " " >> Makefile && \
    echo "build/robot.jar:" >> Makefile && \
    echo "	echo 'skipped ROBOT jar download.....' && touch \$@" >> Makefile && \
    echo "" >> Makefile

# Install KGCL ROBOT plugin
RUN wget -nv -O /tools/robot-plugins/kgcl.jar https://github.com/gouttegd/kgcl-java/releases/download/kgcl-java-$KGCL_JAVA_VERSION/kgcl-robot-plugin-$KGCL_JAVA_VERSION.jar
