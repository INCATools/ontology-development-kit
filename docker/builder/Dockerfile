# Builder image
# Used to build everything that we cannot install in pre-compiled form
# (typically because pre-compiled binaries don't exist for arm64) and
# we don't want to build directly on the final image (to avoid
# cluttering the image with build-time dependencies).
FROM ubuntu:20.04
WORKDIR /build

# Everything that we want to get into one of the final ODK images
# should be installed into one of these directories.
RUN mkdir -p /staging/lite /staging/full

# Install the build tools.
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y \
        build-essential \
        git \
        wget \
        cmake \
        lsb-release \
        clang \
        rustc \
        python3-dev \
        python3-pip

# Build the Python packages.
# On x86_64, most if not all of these packages should be available as
# pre-compiled wheels, so we should not need to build them on a
# separate image; but many of them are *not* available as pre-compiled
# wheels for arm64, so on arm64 they need to be compiled.
# Therefore we install all of them on the builder image (where we have
# all the build tools required to compile them if needed), and we'll
# copy the entire Python tree to the final images.
COPY requirements.txt /build/requirements.txt
COPY requirements.txt.lite /build/requirements.txt.lite
COPY constraints.txt /build/constraints.txt
RUN python3 -m pip install \
        -r /build/requirements.txt.lite \
        -c /build/constraints.txt \
        --root /staging/lite
RUN python3 -m pip install \
        -c /build/constraints.txt \
        -r /build/requirements.txt \
        --root /staging/full

# Compile SWI-Prolog.
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y \
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
        -O /build/swipl-8.2.4.tar.gz && \
    tar xf swipl-8.2.4.tar.gz && \
    cd swipl-8.2.4 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr .. -DSWIPL_PACKAGES_QT=OFF -DSWIPL_PACKAGES_X=OFF && \
    make && \
    make install DESTDIR=/staging/full

# Compile Soufflé.
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y \
        bison \
        doxygen \
        flex \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        mcpp \
        sqlite \
        zlib1g-dev && \
    wget -nv https://github.com/souffle-lang/souffle/archive/refs/tags/2.1.tar.gz \
        -O /build/souffle-2.1.tar.gz && \
    tar xf souffle-2.1.tar.gz && \
    cd souffle-2.1 && \
    cmake -S . -B build && \
    cmake --build build --target install DESTDIR=/staging/full

# Compile Fastobo-validator.
RUN wget -nv https://github.com/fastobo/fastobo-validator/archive/refs/tags/v0.4.0.tar.gz \
        -O /build/fastobo-validator-0.4.0.tar.gz && \
    tar xf fastobo-validator-0.4.0.tar.gz && \
    cd fastobo-validator-0.4.0 && \
    cargo build --release && \
    install -D -m 755 target/release/fastobo-validator /staging/full/usr/bin/fastobo-validator

# Compile Konclude if we are not on x86_64
# (building Konclude is time-consuming, so we avoid it
#  on x86_64 where a pre-compiled binary is available).
ARG TARGETARCH
RUN test "x$TARGETARCH" != xamd64 && (apt-get update && \
        DEBIAN_FRONTEND="noninteractive" apt-get install -y qt5-default wget && \
        wget -nv https://github.com/konclude/Konclude/archive/refs/tags/v0.7.0-1138.tar.gz \
            -O /build/Konclude-0.7.0.tar.gz && \
        tar xf Konclude-0.7.0.tar.gz && \
        cd Konclude-0.7.0-1138 && \
        qmake -r CONFIG+=release CONFIG-=debug CONFIG+=static QT-=gui KoncludeWithoutRedland.pro && \
        make && \
        install -D -m 755 Release/Konclude /staging/full/usr/bin/Konclude \
    ) || true
