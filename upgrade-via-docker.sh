# This is an experimental function to upgrade an existing odk repo to a newer version. Needs ODK repo of version 1.2.13 or higher

echo "This is an experimental update script. It will overwrite your repositories Makefile, update sparql queries and the docker wrapper."

OID=$1
CONFIG=$2
REPOPATH=$3

./seed-via-docker.sh -c -g False -C $CONFIG

cp target/$OID/src/ontology/Makefile $REPOPATH/src/ontology/
cp target/$OID/src/ontology/run.sh $REPOPATH/src/src/ontology/
cp target/$OID/src/sparql/* $REPOPATH/src/sparql/
