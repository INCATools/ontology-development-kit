# The Ontology Development Kit (ODK)

[![Build Status](https://travis-ci.org/INCATools/ontology-development-kit.svg?branch=master)](https://travis-ci.org/INCATools/ontology-development-kit)
[![DOI](https://zenodo.org/badge/48047921.svg)](https://zenodo.org/badge/latestdoi/48047921)


Initialize a Git repo for managing your ontology the OBO Library way!

For more details, see

 * [2018 Article](https://douroucouli.wordpress.com/2018/08/06/new-version-of-ontology-development-kit-now-with-docker-support/)
 * [ICBO Workshop Slides 2018](https://docs.google.com/presentation/d/1nIybviEEJiRKHO2rkBMZsQ0QjtsHyU01_-9beZqD_Z4/edit?usp=sharing)
 * [ICBO Workshop Slides 2017](https://docs.google.com/presentation/d/1JPAaDl6Nitxet9NVqWI30eIygcerYAjdMIGmxbRtIn0/edit?usp=sharing)

# Where to get help

- _How-to guides_:
  - How to [create your first repository](https://github.com/INCATools/ontology-development-kit/blob/master/docs/CreatingRepo.md) with the ODK
  - How to [add license, title and description to your ontology](https://github.com/INCATools/ontology-development-kit/blob/master/docs/License.md)
  - How to [import large ontologies efficiently](https://github.com/INCATools/ontology-development-kit/blob/master/docs/DealWithLargeOntologies.md)
- Reference:
  - Learn about the [different kinds of release artefacts](https://github.com/INCATools/ontology-development-kit/blob/master/docs/ReleaseArtefacts.md)



## Troubleshooting.

If you have issues, file them here: https://github.com/INCATools/ontology-development-kit/issues
We also have an active community on slack, you can request access by making a ticket [here](https://github.com/INCATools/ontology-development-kit/issues) as well

## Customizing

You will likely want to customize the build process, and of course to edit the ontology.

We recommend that you do not edit the main Makefile, but instead the supplemental one (e.g. myont.Makefile) is src/ontology

## Adapting an existing ontology repo

The ODK is designed for creating a new repo for a new ontology. It can still be used to help figure out how to migrate an existing git repository to the ODK structure. There are different ways to do this.

 * Manually compare your ontology against the [template](https://github.com/INCATools/ontology-development-kit/tree/master/template) folder and make necessary adjustments
 * Run the seed script as if creating a new repo. Manually compare this with your existing repo and use `git mv` to rearrange, and adding any missing files by copying them across and doing a `git add`
 * Create a new repo de novo and abandon your existing one, using, for example, github issue mover to move tickets across.
 
Obviously the second method is not ideal as you lose your git history. Note even with `git mv` history tracking becomes harder

If you have built your ontology using a previous version of ODK,
migration of your setup is unfortunately a manual process. In general
you do not absolutely *need* to upgrade your setup, but doing so will
bring advantages in terms of aligning with emerging standards ways of
doing things. The less customization you do on your repo the easier it
should be to migrate.

Consult the [Changes.md](Changes.md) file for changes made between
releases to assist in upgrading.

## More documentation

You will find additional documentation in the src/ontology/README-editors.md file in your repo

## Alternative to Docker

You can run the seed script without docker, you will need Python3.6 or
higher and Java. See requirements.txt for python requirements.

# Running OBO dashboard with ODK

*Note: this is an _highly experimental_ feature as of ODK version 1.2.24. Note that the display and the scores are under active development and will change considerably in the near future.*

Example implementation: 
- https://github.com/obophenotype/obophenotype.github.io ([web](https://obophenotype.github.io/dashboard/index.html))
You need two files to run the ODK dashboard generator:

1. An ODK container wrapper (called `odk.sh` in the following), similar to the `run.sh` file in your typical repos `src/ontology` directory.
2. A dashboard config YAML file (called `dashboard-config.yml` in the following)

With both files, you can then create a dashboard using the following command:

```
sh odk.sh obodash -C dashboard-config.yml
```

The wrapper (`odk.sh`) should contain something like the following:

```
#!/bin/sh
# Wrapper script for ODK docker container.
#
docker run -e ROBOT_JAVA_ARGS='-Xmx4G' -e JAVA_OPTS='-Xmx4G' \
  -v $PWD/dashboard:/tools/OBO-Dashboard/dashboard \
  -v $PWD/dashboard-config.yml:/tools/OBO-Dashboard/dashboard-config.yml \
  -v $PWD/ontologies:/tools/OBO-Dashboard/build/ontologies \
  -v $PWD/sparql:/tools/OBO-Dashboard/sparql \
  -w /work --rm -ti obolibrary/odkfull "$@"
```

Note that this essentially binds a few local directories to the running ODK container. The directories serve the following purposes:

1. `dashboard`: this is where the dashboard is deposited. Look at index.html in your browser.
2. `ontologies`: this is where ontologies are downloaded to and synced up
3. `sparql`: an optional directory that allows you to add custom checks on top of the usual OBO profile.

This is a minimal example dashboard config for a potential phenotype dashboard:

```
title: OBO Phenotype Dashboard
description: Quality control for OBO phenotype ontologies. Under construction.
ontologies:
  custom:
    - id: wbphenotype
    - id: dpo
      base_ns:
        - http://purl.obolibrary.org/obo/FBcv
environment:
  ROBOT_JAR: /tools/robot.jar
  ROBOT: robot
``` 

The ontologies will, if they exist, be retrieved from their OBO purls and evaluated. There are more options potentially of interest:

```
title: OBO Phenotype Dashboard
description: Quality control for OBO phenotype ontologies. Under construction.
ontologies:
  custom:
    - id: myont
      mirror_from: https://raw.githubusercontent.com/obophenotype/c-elegans-phenotype-ontology/master/wbphenotype-base.owl
    - id: dpo
      base_ns:
        - http://purl.obolibrary.org/obo/FBcv
prefer_base: True
profile:
  baseprofile: "https://raw.githubusercontent.com/ontodev/robot/master/robot-core/src/main/resources/report_profile.txt"
  custom:
    - "WARN\tfile:./sparql/missing_xrefs.sparql"
report_truncation_limit: 300
redownload_after_hours: 2
environment:
  ROBOT_JAR: /tools/robot.jar
  ROBOT: robot
``` 

- `mirror_from` allows specifying a download URL other than the default OBO purl
- `base_ns` allows specifying the set of namespaces considered to be _owned_ by the ontology (only terms in these namespaces will be evaluated for this ontology. Default is http://purl.obolibrary.org/obo/CAPTIALISEDONTOLOGYID).
- `report_truncation_limit` allows truncating long (sometimes HUGE ontology reports) to make them go easier on GITHUB version control.
- `redownload_after_hours`: this allows to specify how long to wait before trying to download an ontology (which could be a time consuming process!) again.
- `environment`: is currently a necessary parameter but will be made optional in future versions. It allows adding environment variables directly to the config, rather than passing them in as -e parameters to the docker container (both are equivalent though.)
- `profile` is an optional parameter that allows specifying your own profile for the quality control (ROBOT) report. By default, this is using the ROBOT report default profile. You can either specify your own profile from scratch, or extend the current default with additional test by using the `baseprofile` parameter. Find out more about ROBOT profiles [here](http://robot.obolibrary.org/report#profiles).

A fully working example can be found [here](https://github.com/obophenotype/obophenotype.github.io).
