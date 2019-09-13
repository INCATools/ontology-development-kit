######################################################################
### Config file to allow bulk upgrading of multiple ODKs at once #####
######################################################################

# Currently configured to work on @matentzn setup.

set -e

make docker-build-use-cache
#docker pull obolibrary/odkfull

CONFIGDIR=configs
ROOTDIR=/ws
ROOTDIR_ALT=/Volumes/Nico-EBI/odk_repos_update

# FlyBase
./upgrade-via-docker.sh fbcv $CONFIGDIR/fbcv-odk.yaml $ROOTDIR_ALT/flybase-controlled-vocabulary
./upgrade-via-docker.sh fbbt $CONFIGDIR/fbbt-odk.yaml $ROOTDIR_ALT/drosophila-anatomy-developmental-ontology
./upgrade-via-docker.sh fbdv $CONFIGDIR/fbdv-odk.yaml $ROOTDIR_ALT/drosophila-developmental-ontology
./upgrade-via-docker.sh dpo $CONFIGDIR/dpo-odk.yaml $ROOTDIR/drosophila-phenotype-ontology

# MGI
./upgrade-via-docker.sh mp $CONFIGDIR/mp-odk.yaml $ROOTDIR/mammalian-phenotype-ontology

# ZFIN
./upgrade-via-docker.sh zeco $CONFIGDIR/zeco-odk.yaml $ROOTDIR/zebrafish-experimental-conditions-ontology
./upgrade-via-docker.sh zp $CONFIGDIR/zp-odk.yaml $ROOTDIR_ALT/zebrafish-phenotype-ontology


# Monarch
./upgrade-via-docker.sh hp $CONFIGDIR/hp-odk.yaml $ROOTDIR/human-phenotype-ontology
./upgrade-via-docker.sh maxo $CONFIGDIR/maxo-odk.yaml $ROOTDIR/MAxO
./upgrade-via-docker.sh mo $CONFIGDIR/mo-odk.yaml $ROOTDIR/monarch-ontology
./upgrade-via-docker.sh geno $CONFIGDIR/geno-odk.yaml $ROOTDIR/GENO-ontology
./upgrade-via-docker.sh sepio $CONFIGDIR/sepio-odk.yaml $ROOTDIR/SEPIO-ontology
./upgrade-via-docker.sh ecto $CONFIGDIR/ecto-odk.yaml $ROOTDIR/environmental-exposure-ontology

# OBO Foundry
./upgrade-via-docker.sh cl $CONFIGDIR/cl-odk.yaml $ROOTDIR_ALT/cell-ontology
./upgrade-via-docker.sh nbo $CONFIGDIR/nbo-odk.yaml $ROOTDIR/behavior-ontology
./upgrade-via-docker.sh pato $CONFIGDIR/pato-odk.yaml $ROOTDIR/pato

# Other phenotype ontologies
./upgrade-via-docker.sh ddpheno $CONFIGDIR/ddpheno-odk.yaml $ROOTDIR_ALT/dicty-phenotype-ontology
./upgrade-via-docker.sh xpo $CONFIGDIR/xpo-odk.yaml $ROOTDIR/xenopus-phenotype-ontology
./upgrade-via-docker.sh mgpo $CONFIGDIR/mgpo-odk.yaml $ROOTDIR_ALT/glyco-phenotype-ontology
./upgrade-via-docker.sh fypo $CONFIGDIR/fypo-odk.yaml $ROOTDIR/fypo

# WormBase
./upgrade-via-docker.sh wbbt $CONFIGDIR/wbbt-odk.yaml $ROOTDIR_ALT/c-elegans-gross-anatomy-ontology
./upgrade-via-docker.sh wbls $CONFIGDIR/wbls-odk.yaml $ROOTDIR_ALT/c-elegans-development-ontology
./upgrade-via-docker.sh wbphenotype $CONFIGDIR/wbphenotype-odk.yaml $ROOTDIR/c-elegans-phenotype-ontology

# under construction
# ./seed-via-docker.sh -c -g False -C $CONFIGDIR/sepio-odk.yaml
