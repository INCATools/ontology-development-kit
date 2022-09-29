#!/usr/bin/bash

extra_checks=0
if [ "$1" = "--extra" ]; then
    extra_checks=1
    shift
fi

if [ -z "$1" ]; then
    echo "Usage: ${0##*/} [--extra] FILE"
    exit 10
fi

if [ ! -f "$1" ]; then
    echo "${0##*/}: $1: file not found"
    exit 11
fi

errors=0

echo "Checking RDF/XML file $1..."
echo -n "  LightRDF: "
python3 <<EOF
import sys
from lightrdf import Parser
parser = Parser()
try:
    for triple in parser.parse("$1"):
        pass
except Exception as e:
    print(e)
    sys.exit(1)

print("OK")
EOF
test $? -eq 0 || errors=$(($errors + 1))

if [ $extra_checks -eq 1 ]; then
    echo -n "  RDFLib: "
    if type -p rdfpipe > /dev/null ; then
        if rdfpipe --no-out $1 ; then
            echo "OK"
        else
            errors=$((errors + 1))
        fi
    else
        echo "Not available"
    fi

    echo -n "  Jena: "
    if type -p rdfparse > /dev/null ; then
        # Jena does not return an error code, so we need to capture
        # stderr to detect if an error occured.
        jena_errors=$(rdfparse -s -t $1 2>&1)
        if [ -n "$jena_errors" ]; then
            echo "$jena_errors"
            errors=$(($errors + 1))
        else
            echo "OK"
        fi
    else
        echo "Not available"
    fi
fi

exit $errors
