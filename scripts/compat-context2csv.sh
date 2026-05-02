#!/bin/sh
cat > $$.tmp
exec odk-helper context2csv $$.tmp
rm $$.tmp
