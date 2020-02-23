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

#./upgrade-via-docker.sh hp $CONFIGDIR/hp-odk.yaml $ROOTDIR/human-phenotype-ontology
#./upgrade-via-docker.sh mo $CONFIGDIR/mo-odk.yaml $ROOTDIR/monarch-ontology
#./upgrade-via-docker.sh fypo $CONFIGDIR/fypo-odk.yaml $ROOTDIR/fypo
#./upgrade-via-docker.sh ddpheno $CONFIGDIR/ddpheno-odk.yaml $ROOTDIR/dicty-phenotype-ontology
#./upgrade-via-docker.sh bto $CONFIGDIR/bto-odk.yaml $ROOTDIR/BTO
#./upgrade-via-docker.sh maxo $CONFIGDIR/maxo-odk.yaml $ROOTDIR/MAxO
#cp $ROOTDIR/upheno-dev/src/curation/upheno-config.yaml $CONFIGDIR/upheno-odk.yaml
#./upgrade-via-docker.sh upheno $CONFIGDIR/upheno-odk.yaml $ROOTDIR/upheno-dev
#./upgrade-via-docker.sh xpo $CONFIGDIR/xpo-odk.yaml $ROOTDIR/xenopus-phenotype-ontology
#./upgrade-via-docker.sh planp $CONFIGDIR/planp-odk.yaml $ROOTDIR/planarian-phenotype-ontology
#./upgrade-via-docker.sh phipo $CONFIGDIR/phipo-odk.yaml $ROOTDIR/phipo
#./upgrade-via-docker.sh ecto $CONFIGDIR/ecto-odk.yaml $ROOTDIR/environmental-exposure-ontology
./upgrade-via-docker.sh wbphenotype $CONFIGDIR/wbphenotype-odk.yaml $ROOTDIR/c-elegans-phenotype-ontology
#./seed-via-docker.sh -c -g False -C $CONFIGDIR/wbphenotype-odk.yaml
