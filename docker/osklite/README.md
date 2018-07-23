# osklite

This Docker image is designed to be small. It is designed to be executed once a repo is in place. See the run.sh wrapper in src/ontology

Unlike the main osk container, it does not have git pre-installed. The main osk container needs this for the repo seed step.

# Components

Based on alpine-jdk

 - robot
 - dosdp-tools
 - python dosdp checker??

No owltools or oort