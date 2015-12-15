---
layout: ontology_detail
id: foobar
title: MY-ONTOLOGY-TITLE
jobs:
  - id: https://travis-ci.org/MY-GITHUB-ORG/foobar
    type: travis-ci
build:
  checkout: git clone https://github.com/MY-GITHUB-ORG/foobar.git
  system: git
  path: "."
contact:
  email: cjmungall@lbl.gov
  label: Chris Mungall
description: MY-ONTOLOGY-TITLE is an ontology...
domain: stuff
homepage: https://github.com/MY-GITHUB-ORG/foobar
products:
  - id: foobar.owl
  - id: foobar.obo
dependencies:
 - id: MY-IMPORTED
tracker: https://github.com/MY-GITHUB-ORG/foobar/issues
license:
  url: http://creativecommons.org/licenses/by/3.0/
  label: CC-BY
---

Enter a detailed description of your ontology here
