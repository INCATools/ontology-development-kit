#!/bin/bash

REAL_USER_ID=${ODKUSER_USER_ID:-1000}
REAL_GROUP_ID=${ODKUSER_GROUP_ID:-1000}

groupadd -o -g $REAL_GROUP_ID odkuser
useradd -o -s /bin/bash -u $REAL_USER_ID -g $REAL_GROUP_ID -c "ODK User" -m odkuser
PATH=$PATH:/home/odkuser/.local/bin
[ -d /work ] || mkdir /work
chown -R odkuser:odkuser /work

exec sudo -H -E -u odkuser "$@"
