# This is an experimental function to upgrade an existing odk repo to a newer version. Needs ODK repo of version 1.2.13 or higher

echo "This is an experimental update script. It will overwrite your repositories Makefile, update sparql queries and the docker wrapper."

set -e

OID=$1
CONFIG=$2
REPOPATH=$3
SRCDIR=$REPOPATH/src/

./seed-via-docker.sh -c -g False -C $CONFIG
rsync -r -u --exclude 'patterns/data/default/example.tsv' --exclude 'patterns/dosdp-patterns/example.yaml' --ignore-existing target/$OID/src/ $SRCDIR
cp target/$OID/src/scripts/update_repo.sh $SRCDIR/scripts/
cp target/$OID/src/ontology/Makefile $SRCDIR/ontology/
cp target/$OID/src/ontology/run.sh $SRCDIR/ontology/
cp -r target/$OID/src/sparql/* $SRCDIR/sparql/
