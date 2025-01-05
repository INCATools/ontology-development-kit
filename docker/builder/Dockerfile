# Builder image
# Used to build everything that we cannot install in pre-compiled form
# (typically because pre-compiled binaries don't exist for arm64) and
# we don't want to build directly on the final image (to avoid
# cluttering the image with build-time dependencies).
FROM ubuntu:24.04
WORKDIR /build

# Software versions
ENV RDFTAB_VERSION=0.1.1
ENV SOUFFLE_VERSION=2.4.1
ENV FASTOBO_VALIDATOR_VERSION=0.4.6

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
COPY pip-constraints.txt /build/pip-constraints.txt
RUN find /usr/lib/python3/dist-packages -type d -name '*-info' | \
        sed -E 's,/usr/lib/python3/dist-packages/(.+)-([^-]+)\.(egg|dist)-info,\1==\2,' | \
        sort > pip-constraints.txt.new && \
        if ! cmp -s pip-constraints.txt pip-constraints.txt.new ; then \
             echo "WARNING: Locally derived PIP constraints differ from pre-built constraints!" ;\
             cat pip-constraints.txt.new ;\
        fi
# First the packages needed by the odklite image.
RUN PIP_CONSTRAINT=/build/pip-constraints.txt python3 -m pip install \
        -r /build/requirements.txt.lite \
        -c /build/constraints.txt \
        --no-warn-script-location \
        --root /staging/lite
# Then those needed by the odkfull image.
# After installing those packages, we forcibly remove from the odkfull
# staging tree any file already present in the odklite staging tree
# (caused by packages installed in both trees) to avoid needlessly
# increasing the size of the odkfull image.
RUN PIP_CONSTRAINT=/build/pip-constraints.txt python3 -m pip install \
        -c /build/constraints.txt \
        -r /build/requirements.txt \
        --no-warn-script-location \
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
    wget -nv https://github.com/souffle-lang/souffle/archive/refs/tags/$SOUFFLE_VERSION.tar.gz \
        -O /build/souffle-$SOUFFLE_VERSION.tar.gz && \
    tar xf souffle-$SOUFFLE_VERSION.tar.gz && \
    cd souffle-$SOUFFLE_VERSION && \
    cmake -S . -B build -DSOUFFLE_DOMAIN_64BIT=ON && \
    cmake --build build --target install DESTDIR=/staging/full && \
    cd /build && \
    rm -rf souffle-$SOUFFLE_VERSION souffle-$SOUFFLE_VERSION.tar.gz

# Compile Fastobo-validator.
RUN wget -nv https://github.com/fastobo/fastobo-validator/archive/refs/tags/v$FASTOBO_VALIDATOR_VERSION.tar.gz \
        -O /build/fastobo-validator-$FASTOBO_VALIDATOR_VERSION.tar.gz && \
    tar xf fastobo-validator-$FASTOBO_VALIDATOR_VERSION.tar.gz && \
    cd fastobo-validator-$FASTOBO_VALIDATOR_VERSION && \
    cargo build --release -Z sparse-registry && \
    install -D -m 755 target/release/fastobo-validator /staging/full/usr/bin/fastobo-validator && \
    cd /build && \
    rm -rf fastobo-validator-$FASTOBO_VALIDATOR_VERSION fastobo-validator-$FASTOBO_VALIDATOR_VERSION.tar.gz /root/.cargo

# Compile rdftab.
RUN wget -nv https://github.com/ontodev/rdftab.rs/archive/refs/tags/v$RDFTAB_VERSION.tar.gz \
        -O /build/rdftab.tar.gz && \
    tar xf rdftab.tar.gz && \
    cd rdftab.rs-$RDFTAB_VERSION && \
    cargo build --release -Z sparse-registry && \
    install -D -m 755 target/release/rdftab /staging/lite/usr/bin/rdftab && \
    cd /build && \
    rm -rf rdftab.rs-$RDFTAB_VERSION rdftab.tar.gz /root/.cargo
