#!/bin/sh
ODK_DEBUG_FILE=${ODK_DEBUG_FILE:-debug.log}
echo "Command: sh $@" >> $ODK_DEBUG_FILE
/usr/bin/time -a -o $ODK_DEBUG_FILE -f "Elapsed time: %E\nPeak memory: %M kb" /bin/sh "$@"
