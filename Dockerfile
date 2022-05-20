# Final ODK image
# (built upon the odklite image)
FROM obolibrary/odklite:latest
LABEL maintainer="obo-tools@googlegroups.com"

ENV PATH "/tools/apache-jena/bin:/tools/sparqlprog/bin:$PATH"

ARG ODK_VERSION 0.0.0
ENV ODK_VERSION $ODK_VERSION

# Avoid repeated downloads of script dependencies by mounting the local coursier cache:
# docker run -v $HOME/.coursier/cache/v1:/tools/.coursier-cache ...
ENV COURSIER_CACHE "/tools/.coursier-cache"

# Install GH
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null

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
    sqlite3 \
    libjson-perl \
    pkg-config \
    xlsx2csv \
    gh \
    nodejs \
    npm \
    graphviz \
    python3-psycopg2

# Install run-time dependencies for SWI-Prolog.
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
# On x86_64, we get it from a pre-built release; on arm64, we
# have built it in the builder image, now we need to install
# the run-time dependencies (Qt5).
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
            libqt5xml5 libqt5network5 libqt5concurrent5 \
    )

# Install Jena.
RUN wget -nv http://archive.apache.org/dist/jena/binaries/apache-jena-3.12.0.tar.gz -O- | tar xzC /tools && \
    mv /tools/apache-jena-3.12.0 /tools/apache-jena

# Install SPARQLProg.
RUN swipl -g "pack_install(sparqlprog, [interactive(false)])" -g halt && \
    ln -sf /root/.local/share/swi-prolog/pack/sparqlprog /tools/

# Install obographviz
RUN npm install obographviz && \
    ln -s /tools/node_modules/obographviz/bin/og2dot.js /tools/og2dot.js

# Install OBO-Dashboard.
COPY scripts/obodash /tools
RUN chmod +x /tools/obodash && \
    git clone --depth 1 https://github.com/OBOFoundry/OBO-Dashboard.git && \
    cd OBO-Dashboard && \
    python3 -m pip install -r requirements.txt && \
    echo " " >> Makefile && \
    echo "build/robot.jar:" >> Makefile && \
    echo "	echo 'skipped ROBOT jar download' && touch \$@" >> Makefile && \
    echo "" >> Makefile

# Install relation-graph
ENV RG=2.1.0
ENV PATH "/tools/relation-graph/bin:$PATH"
RUN wget -nv https://github.com/balhoff/relation-graph/releases/download/v$RG/relation-graph-$RG.tgz \
&& tar -zxvf relation-graph-$RG.tgz \
&& mv relation-graph-$RG /tools/relation-graph \
&& chmod +x /tools/relation-graph
