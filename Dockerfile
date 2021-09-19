# Builder image
# Used to build everything that we cannot install in pre-compiled form (typically
# because pre-compiled binaries don't exist for arm64) and we don't want to build
# directly on the final image (to avoid cluttering the image with build-time
# dependencies).
FROM ubuntu:20.04 AS builder
WORKDIR /tools
RUN mkdir -p /tools/staging

# Compile SWI-Prolog
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y \
        build-essential \
        wget \
        cmake \
        ncurses-dev \
        libreadline-dev \
        libedit-dev \
        libgoogle-perftools-dev \
        libunwind-dev \
        libgmp-dev \
        libssl-dev \
        unixodbc-dev \
        zlib1g-dev \
        libarchive-dev \
        libxext-dev \
        libice-dev \
        libjpeg-dev \
        libxinerama-dev \
        libxft-dev \
        libxpm-dev \
        libxt-dev \
        libdb-dev \
        libpcre3-dev \
        libyaml-dev \
        junit4 && \
    wget -nv https://www.swi-prolog.org/download/stable/src/swipl-8.2.4.tar.gz \
        -O /tools/swipl-8.2.4.tar.gz && \
    cd /tools && \
    tar xf swipl-8.2.4.tar.gz && \
    cd swipl-8.2.4 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr .. -DSWIPL_PACKAGES_QT=OFF -DSWIPL_PACKAGES_X=OFF && \
    make && \
    make install DESTDIR=/tools/staging

# Compile Soufflé
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y \
        build-essential \
        wget \
        git \
        bison \
        clang \
        cmake \
        doxygen \
        flex \
        g++ \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        mcpp \
        sqlite \
        lsb-release \
        zlib1g-dev && \
    wget -nv https://github.com/souffle-lang/souffle/archive/refs/tags/2.1.tar.gz \
        -O /tools/souffle-2.1.tar.gz && \
    tar xf souffle-2.1.tar.gz && \
    cd souffle-2.1 && \
    cmake -S . -B build && \
    cmake --build build --target install DESTDIR=/tools/staging

# Final ODK image
# Built upon the odklite image
FROM obolibrary/odklite:latest
LABEL maintainer="obo-tools@googlegroups.com"

ENV FASTOBO_VERSION 0.4.0
ENV JENA_VERSION 3.12.0

ENV PATH "/tools/apache-jena/bin:/tools/sparqlprog/bin:$PATH"

ARG ODK_VERSION 0.0.0
ENV ODK_VERSION $ODK_VERSION

# Avoid repeated downloads of script dependencies by mounting the local coursier cache:
# docker run -v $HOME/.coursier/cache/v1:/tools/.coursier-cache ...
ENV COURSIER_CACHE "/tools/.coursier-cache"

# Tools provided by Ubuntu
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
    build-essential \
    openjdk-8-jdk-headless \
    maven \
    python-dev \
    subversion \
    automake \
    aha \
    dos2unix \
    sqlite3 \
    libjson-perl \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    xlsx2csv

# Python environment
COPY requirements.txt /tools
RUN python3 -m pip install -r /tools/requirements.txt -c /tools/constraints.txt && \
    rm -rf /root/.cache

# SWI-Prolog runtime dependencies
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        libarchive13 \
        libedit2 \
        libgmp10 \
        libossp-uuid16 \
        libpcre3 \
        libreadline8 \
        libssl1.1 \
        libtinfo6 \
        zlib1g \
        libedit-dev \
        libgmp-dev \
        libjs-jquery \
        libncursesw5-dev \
        libreadline-dev \
        libtcmalloc-minimal4

# Soufflé runtime dependencies
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        g++ \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        mcpp \
        zlib1g-dev

# Copy everything that we have built in the builder image
# (for now, SWI-Prolog and Soufflé)
COPY --from=builder /tools/staging /

# Konclude
# FIXME: This won't work on arm64, we need to build it from source in the
#        builder image and copy it from there
RUN wget -nv https://github.com/konclude/Konclude/releases/download/v0.6.2-845/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13.zip \
        -O /tools/konclude.zip && \
    unzip /tools/konclude.zip && \
    mv /tools/Konclude-v0.6.2-845-LinuxAlpine-x64-GCC8.3.0-Static-Qt-5.13 /tools/konclude_reasoner && \
    rm /tools/konclude.zip && \
    chmod +x /tools/konclude_reasoner/Binaries && \
    echo "#!/bin/bash" > /tools/Konclude && \
    echo '/tools/konclude_reasoner/Binaries/Konclude $*' >> /tools/Konclude && \
    chmod +x /tools/Konclude

# FASTOBO
# FIXME: This won't work on arm64, we need to build it from source in the
#        builder image and copy it from there
RUN wget -nv https://github.com/fastobo/fastobo-validator/releases/download/v$FASTOBO_VERSION/fastobo_validator-x86_64-linux-musl.tar.gz -O- | tar zxC /tools && \
    chmod 755 /tools/fastobo-validator

# JENA
RUN wget -nv http://archive.apache.org/dist/jena/binaries/apache-jena-$JENA_VERSION.tar.gz -O- | tar xzC /tools && \
    mv /tools/apache-jena-$JENA_VERSION /tools/apache-jena

# SPARQLProg
RUN swipl -g "pack_install(sparqlprog, [interactive(false)])" -g halt
RUN ln -sf /root/.local/share/swi-prolog/pack/sparqlprog /tools/

# OBO-Dashboard
COPY scripts/obodash /tools
RUN chmod +x /tools/obodash && \
    git clone --depth 1 https://github.com/OBOFoundry/OBO-Dashboard.git && \
    cd OBO-Dashboard && \
    python3 -m pip install -r requirements.txt && \
    echo " " >> Makefile && \
    echo "build/robot.jar:" >> Makefile && \
    echo "	echo 'skipped ROBOT jar download' && touch \$@" >> Makefile && \
    echo "" >> Makefile
