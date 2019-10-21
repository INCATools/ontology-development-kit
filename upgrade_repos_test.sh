######################################################################
### Config file to allow bulk upgrading of multiple ODKs at once #####
######################################################################

# Currently configured to work on @matentzn setup.

set -e

make docker-build-use-cache
#docker pull obolibrary/odkfull

CONFIGDIR=configs
ROOTDIR=~/ws
ROOTDIR_ALT=/Volumes/Nico-EBI/odk_repos_update

./upgrade-via-docker.sh dpo $CONFIGDIR/dpo-odk.yaml $ROOTDIR/drosophila-phenotype-ontology
./upgrade-via-docker.sh mp $CONFIGDIR/mp-odk.yaml $ROOTDIR/mammalian-phenotype-ontology
