FROM obolibrary/odklite:latest
ARG TARGETARCH
RUN test "x$TARGETARCH" = xamd64 && echo "AMD64" > /architecture.txt || echo "ARM64" > /etc/architecture.txt

