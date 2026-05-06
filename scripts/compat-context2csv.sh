#!/bin/sh
cat > $$.tmp
odk-helper context2csv $$.tmp
rc=$?
rm $$.tmp
exit $rc
