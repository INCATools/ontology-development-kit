#!/bin/sh
cat > $$.tmp
odk-helper context2csv $$.tmp
rm $$.tmp
