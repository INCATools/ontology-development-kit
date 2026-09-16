# odklite

This Docker image is designed to be small. It is designed to be executed once a repo is in place. See the run.sh wrapper in src/ontology

# Components

Based on Ubuntu 26.04 with a JRE installed.

 - robot
 - dosdp-tools
 - relation-graph
 - dicer-cli
 - sssom-cli

The owltools and oort tools are not provided in this image; use the odkfull image if you need them.
