#!/usr/bin/bash

check_lightrdf=1
check_rdflib=0
check_jena=0
rdfxml_file=

while [ -n "$1" ]; do
    case "$1" in
    --lightrdf)
        check_lightrdf=1
        shift
        ;;

    --no-lightrdf)
        check_lightrdf=0
        shift
        ;;

    --rdflib)
        check_rdflib=1
        shift
        ;;

    --no-rdflib)
        check_rdflib=0
        shift
        ;;

    --jena)
        check_jena=1
        shift
        ;;

    --no-jena)
        check_jena=0
        shift
        ;;

    *)
        rdfxml_file=$1
        shift
        ;;
    esac
done

if [ -z "$rdfxml_file" ]; then
    echo "Usage: ${0##*/} [[--no-]lightrdf] [[--no-]rdflib] [[--no-]jena] FILE"
    exit 10
fi

if [ ! -f "$rdfxml_file" ]; then
    echo "${0##*/}: $rdfxml_file: file not found"
    exit 11
fi

errors=0

echo "Checking RDF/XML file $rdfxml_file..."

if [ $check_lightrdf -eq 1 ]; then
    echo -n "  LightRDF: "
    python3 <<EOF
import sys
from lightrdf import Parser
parser = Parser()
try:
    for triple in parser.parse("$rdfxml_file"):
        pass
except Exception as e:
    print(e)
    sys.exit(1)

print("OK")
EOF
    test $? -eq 0 || errors=$(($errors + 1))
fi

if [ $check_rdflib -eq 1 ]; then
    echo -n "  RDFLib: "
    if type -p rdfpipe > /dev/null ; then
        if rdfpipe --no-out $rdfxml_file ; then
            echo "OK"
        else
            errors=$((errors + 1))
        fi
    else
        echo "Not available"
    fi
fi

if [ $check_jena -eq 1 ]; then
    echo -n "  Jena: "
    if type -p riot > /dev/null ; then
        if riot --validate $rdfxml_file ; then
            echo "OK"
        else
            errors=$((errors + 1))
        fi
    else
        echo "Not available"
    fi
fi

exit $errors
