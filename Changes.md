# 1.1.1

## Changes

Name of repo has changed to ontology-developer-kit

 * changing name of docker image to odk
 * Upgrade dosdp-tools to release 0.9.
 * Make docker commands workable on windows
 * Dockerize travis
 * Imports automatically generated
 * Added python dosdp checker to docker, fixes #55
 * use robot not owltools in all places

## Migration guide

If you built your repo from a previous version of ODK, here is a rough guide to migrating:

 * Update your .travis.yml, in order to use Docker (optional but recommended)
 * change the name of the docker image to odkfull in your run.sh

# 1.1.0

 * Add a run.sh in the template for Docker