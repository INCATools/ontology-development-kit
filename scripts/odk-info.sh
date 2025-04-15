#!/bin/bash

show_odk_version=1
show_tools_version=0
show_all_python_packages=0

while [ -n "$1" ]; do
case $1 in
--tools)
    show_tools_version=1
    shift
    ;;

--all-python)
    show_all_python_packages=1
    shift
    ;;

--all)
    show_tools_version=1
    show_all_python_packages=1
    shift
    ;;

*)
    echo "Usage: odk-info [--tools|--all-python|--all]"
    exit
    ;;
esac
done

if [ $show_odk_version -eq 1 ]; then
    echo "ODK Image @@ODK_IMAGE_VERSION@@"
fi

if [ $show_tools_version -eq 1 ]; then
    robot --version
    echo "DOSDP-Tools v$(dosdp-tools --version | sed -ne 's/^.*version: //;s/,.*$//p')"
    if type -p Konclude > /dev/null ; then
        echo "Konclude $(Konclude -h | sed -nre 's/^.*Version (.*) - .*$/\1/p')"
    fi
    if type -p jena.version > /dev/null ; then
        echo "Jena v$(jena.version)"
    fi
    if type -p relation-graph > /dev/null ; then
        echo "Relation-Graph v$(relation-graph --version | sed -ne 's/^.*version: //;s/,.*$//p')"
    fi
    if type -p runoak > /dev/null ; then
        echo "Ontology Access Kit v$(python3 -m pip show oaklib | sed -ne 's/^Version: //p')"
    fi
    if type -p amm > /dev/null ; then
        amm --version
    fi
    if type -p sssom-cli > /dev/null ; then
        sssom-cli --version | sed -ne 's/^sssom-cli (SSSOM-Java \(.*\))/SSSOM-CLI version \1/p'
    fi
fi

if [ $show_all_python_packages -eq 1 ]; then
    echo "Python packages:"
    python3 -m pip list
fi
