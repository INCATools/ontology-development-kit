#!/bin/bash

if [ -z "$ODK_USER_ID" -o "$ODK_USER_ID" = 0 ]; then
    exec "$@"
fi

REAL_USER_ID=${ODK_USER_ID:-1000}
REAL_GROUP_ID=${ODK_GROUP_ID:-1000}

groupadd -o -g $REAL_GROUP_ID odkuser
useradd -o -s /bin/bash -u $REAL_USER_ID -g $REAL_GROUP_ID -c "ODK User" -M odkuser
mkdir -p /home/odkuser
chown odkuser:odkuser /home/odkuser
[ -d /home/odkuser/.data ] && chown odkuser:odkuser /home/odkuser/.data
[ -d /home/odkuser/.data/oaklib ] && chown odkuser:odkuser /home/odkuser/.data/oaklib
if [ ! -d /tools/.coursier-cache ] ; then
    mkdir /tools/.coursier-cache
    chown odkuser:odkuser /tools/.coursier-cache
fi
PATH=$PATH:/home/odkuser/.local/bin
[ -S /run/host-services/ssh-auth.sock ] && chown odkuser /run/host-services/ssh-auth.sock

exec sudo -H -E -u odkuser "$@"
