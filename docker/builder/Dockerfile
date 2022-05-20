# Builder image
# Used to build everything that we cannot install in pre-compiled form
# (typically because pre-compiled binaries don't exist for arm64) and
# we don't want to build directly on the final image (to avoid
# cluttering the image with build-time dependencies).
FROM ubuntu:22.04
WORKDIR /build

# Software versions
ENV RDFTAB_VERSION=0.1.1

# Everything that we want to get into one of the final ODK images
# should be installed into one of these directories.
RUN mkdir -p /staging/lite /staging/full

# Install the build tools.
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        build-essential \
        git \
        wget \
        cmake \
        lsb-release \
        clang \
        rustc \
        cargo \
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
COPY requirements.txt.full /build/requirements.txt
COPY requirements.txt.lite /build/requirements.txt.lite
COPY constraints.txt /build/constraints.txt
# First the packages needed by the odklite image.
RUN python3 -m pip install \
        -r /build/requirements.txt.lite \
        -c /build/constraints.txt \
        --root /staging/lite
# Then those needed by the odkfull image.
# After installing those packages, we forcibly remove from the odkfull
# staging tree any file already present in the odklite staging tree
# (caused by packages installed in both trees) to avoid needlessly
# increasing the size of the odkfull image.
RUN python3 -m pip install \
        -c /build/constraints.txt \
        -r /build/requirements.txt \
        --root /staging/full && \
        cd /staging/lite && \
        find . -type f | while read f ; do rm -f /staging/full/$f ; done && \
        find . -type d -depth | while read f ; do rmdir /staging/full/$f || true ; done

# Compile Soufflé.
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        bison \
        doxygen \
        flex \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        mcpp \
        sqlite3 \
        zlib1g-dev && \
    wget -nv https://github.com/souffle-lang/souffle/archive/refs/tags/2.1.tar.gz \
        -O /build/souffle-2.1.tar.gz && \
    tar xf souffle-2.1.tar.gz && \
    cd souffle-2.1 && \
    cmake -S . -B build && \
    cmake --build build --target install DESTDIR=/staging/full && \
    cd /build && \
    rm -rf souffle-2.1 souffle-2.1.tar.gz

# Compile Fastobo-validator.
RUN wget -nv https://github.com/fastobo/fastobo-validator/archive/refs/tags/v0.4.0.tar.gz \
        -O /build/fastobo-validator-0.4.0.tar.gz && \
    tar xf fastobo-validator-0.4.0.tar.gz && \
    cd fastobo-validator-0.4.0 && \
    cargo build --release && \
    install -D -m 755 target/release/fastobo-validator /staging/full/usr/bin/fastobo-validator && \
    cd /build && \
    rm -rf fastobo-validator-0.4.0 fastobo-validator-0.4.0.tar.gz /root/.cargo

# Compile rdftab.
RUN wget -nv https://github.com/ontodev/rdftab.rs/archive/refs/tags/v$RDFTAB_VERSION.tar.gz \
        -O /build/rdftab.tar.gz && \
    tar xf rdftab.tar.gz && \
    cd rdftab.rs-$RDFTAB_VERSION && \
    cargo build --release && \
    install -D -m 755 target/release/rdftab /staging/full/usr/bin/rdftab && \
    cd /build && \
    rm -rf rdftab.rs-$RDFTAB_VERSION rdftab.tar.gz /root/.cargo

# Compile Konclude if we are not on x86_64
# (building Konclude is time-consuming, so we avoid it
#  on x86_64 where a pre-compiled binary is available).
ARG TARGETARCH
RUN test "x$TARGETARCH" != xamd64 && (apt-get update && \
        DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
            qtbase5-dev qt5-qmake qtbase5-dev-tools wget && \
        wget -nv https://github.com/konclude/Konclude/archive/refs/tags/v0.7.0-1138.tar.gz \
            -O /build/Konclude-0.7.0.tar.gz && \
        tar xf Konclude-0.7.0.tar.gz && \
        cd Konclude-0.7.0-1138 && \
        qmake -r CONFIG+=release CONFIG-=debug CONFIG+=static QT-=gui KoncludeWithoutRedland.pro && \
        make && \
        install -D -m 755 Release/Konclude /staging/full/usr/bin/Konclude && \
        cd /build && \
        rm -rf Konclude-0.7.0-1138 Konclude-0.7.0.tar.gz \
    ) || true
