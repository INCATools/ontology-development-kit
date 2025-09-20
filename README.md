[![Build the ODK images and run the tests](https://github.com/INCATools/ontology-development-kit/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/INCATools/ontology-development-kit/actions/workflows/build-and-test.yml)
[![DOI](https://zenodo.org/badge/48047921.svg)](https://zenodo.org/badge/latestdoi/48047921)
[![DOI](https://img.shields.io/docker/pulls/obolibrary/odkfull.svg)](https://hub.docker.com/r/obolibrary/odkfull)


https://www.wikidata.org/wiki/Q112336713

# The Ontology Development Kit (ODK)

<img src="https://github.com/jmcmurry/closed-illustrations/raw/master/logos/odk-logos/odk-logo_black-banner.png" />

Manage your ontology's life cycle with the Ontology Development Kit (ODK)! The ODK is
- a toolbox of various ontology related tools such as ROBOT, owltools, dosdp-tools and many more, bundled as a docker image
- a set of executable workflows for managing your ontology's continuous integration, quality control, releases and dynamic imports

For more details, see

 * [2022 Paper](https://doi.org/10.1093/database/baac087)
 * [2018 Article](https://douroucouli.wordpress.com/2018/08/06/new-version-of-ontology-development-kit-now-with-docker-support/)
 * [ICBO Workshop Slides 2018](https://docs.google.com/presentation/d/1nIybviEEJiRKHO2rkBMZsQ0QjtsHyU01_-9beZqD_Z4/edit?usp=sharing)
 * [ICBO Workshop Slides 2017](https://docs.google.com/presentation/d/1JPAaDl6Nitxet9NVqWI30eIygcerYAjdMIGmxbRtIn0/edit?usp=sharing)

# Where to get help

- _How-to guides_:
  - How to [create your first repository](https://oboacademy.github.io/obook/howto/odk-create-repo/) with the ODK
  - How to [add license, title and description to your ontology](https://oboacademy.github.io/obook/reference/formatting-license/)
  - How to [import large ontologies efficiently](https://oboacademy.github.io/obook/howto/deal-with-large-ontologies/)
- Reference:
  - Learn about the [different kinds of release artefacts](https://oboacademy.github.io/obook/reference/release-artefacts/)
  - Learn about the [ODK Project Configuration Schema](https://github.com/INCATools/ontology-development-kit/blob/master/docs/project-schema.md) for allowed parameters in your `[project]-odk.yaml`
- Community:
  -  If you have issues, file them here: https://github.com/INCATools/ontology-development-kit/issues
  -  We also have an active community on Slack; you can request access by making a ticket [here](https://github.com/INCATools/ontology-development-kit/issues) as well

# Steering Committee

* @gouttegd Damien Goutte-Gattat (ODK Lead, FlyBase)
* @matentzn Nicolas Matentzoglu (ODK Deputy, Semanticly)
* @cmungall Chris Mungall (ODK Founder, LBNL)

# Core team

* @anitacaron Anita Caron (Novo Nordisk)
* @balhoff Jim Balhoff (RENCI)
* @dosumis David Osumi-Sutherland (Sanger)
* @ehartley Emily Hartley (Critical Path Institute)
* @hkir-dev Huseyin Kir (EMBL-EBI)
* @shawntanzk Shawn Tan (Novo Nordisk)
* @ubyndr Ismail Ugur Bayindir (EMBL-EBI)

Full list of contributors:
https://github.com/INCATools/ontology-development-kit/graphs/contributors

# Cite

https://doi.org/10.1093/database/baac087

# Outstanding contributions
Outstanding contributors are groups and institutions that have helped with organising the ODK development, providing funding,
advice and infrastructure. We are very grateful for all your contributions - the project would not exist without you!

## Monarch Initiative
<img src="https://user-images.githubusercontent.com/7070631/121600493-72ee4b00-ca3c-11eb-87c3-57742fca7af5.png" data-canonical-src="https://user-images.githubusercontent.com/7070631/121600493-72ee4b00-ca3c-11eb-87c3-57742fca7af5.png" width="300" />

The Monarch Initiative is a consortium of medical, biological and computational experts that provide major ontology services such as the Human Phenotype Ontology, [Mondo](https://mondo.monarchinitiative.org/) and an integrative data and [analytic platform](https://monarchinitiative.org/) connecting phenotypes to genotypes across species, bridging basic and applied research with semantics-based analysis.

https://monarchinitiative.org/

## European Bioinformatics Institute
<img src="https://user-images.githubusercontent.com/7070631/121600529-813c6700-ca3c-11eb-8590-871a963a3cfd.png" data-canonical-src="https://user-images.githubusercontent.com/7070631/121600529-813c6700-ca3c-11eb-8590-871a963a3cfd.png" width="300" />

The Samples, Phenotypes and Ontologies (SPOT) team, led by Helen Parkinson, is concerned with high throughput mammalian phenotyping, Semantics as a Service and human genetics resources. Members of the SPOT team including David Osumi-Sutherland have made major contributions to ODK, and provided advice, use cases and funding.

https://www.ebi.ac.uk/spot/

## University of Florida Biomedical Informatics Program
<img src="https://user-images.githubusercontent.com/7070631/121600373-46d2ca00-ca3c-11eb-8899-c814c4041d54.png" data-canonical-src="https://user-images.githubusercontent.com/7070631/121600373-46d2ca00-ca3c-11eb-8899-c814c4041d54.png" width="300" />

https://hobi.med.ufl.edu/research-2/biomedical-informatics-3/

## Knocean Inc.
<img src="https://user-images.githubusercontent.com/7070631/121600426-56eaa980-ca3c-11eb-9315-b03234bb6b06.png" data-canonical-src="https://user-images.githubusercontent.com/7070631/121600426-56eaa980-ca3c-11eb-9315-b03234bb6b06.png" width="300" />

Knocean Inc. offers consulting and development services for science informatics, in particular in the area of biomedical ontologies and ontology tooling.

http://knocean.com/

## Critical Path Institute
<img src="https://user-images.githubusercontent.com/7070631/122019745-049ee500-cdbc-11eb-9ed0-3ac3ca717d9b.png" data-canonical-src="https://user-images.githubusercontent.com/7070631/122019745-049ee500-cdbc-11eb-9ed0-3ac3ca717d9b.png" width="300" />

The Critical Path For Alzheimer’s Disease (CPAD) is a public-private partnership aimed at creating new tools and methods that can be applied to increase the efficiency of the development process of new treatments for Alzheimer disease (AD) and related neurodegenerative disorders with impaired cognition and function.

https://c-path.org/

# Requirements

## Docker

Using the ODK docker image requires Docker Engine version 20.10.8 or greater for v1.3.1.

# Tips and Tricks

## Customizing your ODK installation

You will likely want to customize the build process, and of course to edit the ontology.

We recommend that you do not edit the main Makefile, but instead the supplemental one (e.g. myont.Makefile) is src/ontology

An example of how you can customise your imports for example is documented [here](http://pato-ontology.github.io/pato/odk-workflows/RepoManagement/)

## Migrating an existing ontology repo to the ODK

The ODK is designed for creating a new repo for a new ontology. It can also be used to help figure out how to migrate an existing git repository to the ODK structure. There are different ways to do this.

 * Manually compare your ontology against the [template](https://github.com/INCATools/ontology-development-kit/tree/master/template) folder and make necessary adjustments
 * Run the seed script as if creating a new repo. Manually compare this with your existing repo and use `git mv` to rearrange, and adding any missing files by copying them across and doing a `git add`
 * Create a new repo de novo and abandon your existing one, using, for example, github issue mover to move tickets across.

Obviously the second method is not ideal as you lose your git history. Note even with `git mv` history tracking becomes harder.

If you have built your ontology using a previous version of ODK,
migration of your setup is unfortunately a manual process. In general
you do not absolutely *need* to upgrade your setup, but doing so will
bring advantages in terms of aligning with emerging standards ways of
doing things. The less customization you do on your repo the easier it
should be to migrate.

Consult the [CHANGELOG.md](CHANGELOG.md) file for changes made between
releases to assist in upgrading.

## More documentation

You will find additional documentation in the src/ontology/README-editors.md file in your repo.

The ODK also comes with built in options to generate your own shiny documentation; see for example the [PATO documentation here](http://pato-ontology.github.io/pato/) which is almost entirely autogenerated from the ODK.

## Alternative to Docker

You can run the seed script without docker using Python3.6 or
higher and Java. See requirements.txt for python requirements.

*This is, however, not recommended.*
