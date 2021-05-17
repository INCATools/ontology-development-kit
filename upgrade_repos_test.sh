######################################################################
### Config file to allow bulk upgrading of multiple ODKs at once #####
######################################################################

# Currently configured to work on @matentzn setup.

set -e

#make docker-build
#docker pull obolibrary/odkfull

CONFIGDIR=configs
ROOTDIR=~/ws
ROOTDIR_ALT=/Volumes/Nico-EBI/odk_repos_update

#./upgrade-via-docker.sh mp $CONFIGDIR/mp-odk.yaml $ROOTDIR/mammalian-phenotype-ontology
#./upgrade-via-docker.sh nbo $CONFIGDIR/nbo-odk.yaml $ROOTDIR/behavior-ontology
#./upgrade-via-docker.sh uberon $CONFIGDIR/uberon-odk.yaml ~/knocean/uberon
#./upgrade-via-docker.sh dron $CONFIGDIR/dron-odk.yaml $ROOTDIR/dron
#./upgrade-via-docker.sh mo $CONFIGDIR/mo-odk.yaml $ROOTDIR/monarch-ontology
#./upgrade-via-docker.sh fypo $CONFIGDIR/fypo-odk.yaml $ROOTDIR/fypo
#./upgrade-via-docker.sh ddpheno $CONFIGDIR/ddpheno-odk.yaml $ROOTDIR/dicty-phenotype-ontology
#./upgrade-via-docker.sh bto $CONFIGDIR/bto-odk.yaml $ROOTDIR/BTO
#./upgrade-via-docker.sh maxo $CONFIGDIR/maxo-odk.yaml $ROOTDIR/MAxO
#cp $ROOTDIR/upheno-dev/src/curation/upheno-config.yaml $CONFIGDIR/upheno-odk.yaml
./upgrade-via-docker.sh upheno $CONFIGDIR/upheno-odk.yaml $ROOTDIR/upheno
#./upgrade-via-docker.sh xpo $CONFIGDIR/xpo-odk.yaml $ROOTDIR/xenopus-phenotype-ontology
#./upgrade-via-docker.sh planp $CONFIGDIR/planp-odk.yaml $ROOTDIR/planarian-phenotype-ontology
#./upgrade-via-docker.sh phipo $CONFIGDIR/phipo-odk.yaml $ROOTDIR/phipo
#./upgrade-via-docker.sh ecto $CONFIGDIR/ecto-odk.yaml $ROOTDIR/environmental-exposure-ontology
#./upgrade-via-docker.sh wbphenotype $CONFIGDIR/wbphenotype-odk.yaml $ROOTDIR/c-elegans-phenotype-ontology
#./upgrade-via-docker.sh wbls $CONFIGDIR/wbls-odk.yaml $ROOTDIR/c-elegans-development-ontology
#./upgrade-via-docker.sh wbbt $CONFIGDIR/wbbt-odk.yaml $ROOTDIR/c-elegans-gross-anatomy-ontology
#./upgrade-via-docker.sh cl $CONFIGDIR/cl-odk.yaml ~/knocean/cell-ontology
#./upgrade-via-docker.sh zp $CONFIGDIR/zp-odk.yaml ~/ws/zebrafish-phenotype-ontology
#./upgrade-via-docker.sh pato $CONFIGDIR/pato-odk.yaml $ROOTDIR/pato
#./upgrade-via-docker.sh zeco $CONFIGDIR/zeco-odk.yaml $ROOTDIR/zebrafish-experimental-conditions-ontology
#./seed-via-docker.sh -c -g False -C $CONFIGDIR/wbphenotype-odk.yaml
#./upgrade-via-docker.sh dpo $CONFIGDIR/dpo-odk.yaml $ROOTDIR/drosophila-phenotype-ontology
#./upgrade-via-docker.sh geno $CONFIGDIR/geno-odk.yaml $ROOTDIR/GENO-ontology
#./upgrade-via-docker.sh covoc $CONFIGDIR/covoc-odk.yaml $ROOTDIR/covoc
#./upgrade-via-docker.sh chr $CONFIGDIR/chr-odk.yaml $ROOTDIR/monochrom
