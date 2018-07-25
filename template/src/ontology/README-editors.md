These notes are for the EDITORS of foobar

This project was created using the [ontology starter kit](https://github.com/cmungall/ontology-starter-kit). See the site for details.

For more details on ontology management, please see the [OBO tutorial](https://github.com/jamesaoverton/obo-tutorial) or the [Gene Ontology Editors Tutorial](go-protege-tutorial.readthedocs.io)

You may also want to read the [GO ontology editors guide](http://go-ontology.readthedocs.org/)

## Requirements

 1. Protege (for editing)
 2. A git client (we assume command line git)
 3. [docker](https://www.docker.com/get-docker) (for managing releases)

## Editors Version

Make sure you have an ID range in the [idranges file](foobar-idranges.owl)

If you do not have one, get one from the head curator.

The editors version is [foobar-edit.owl](foobar-edit.owl)

** DO NOT EDIT foobar.obo OR foobar.owl in the top level directory **

[../../foobar.owl](../../foobar.owl) is the release version

To edit, open the file in Protege. First make sure you have the repository cloned, see [the GitHub project](https://github.com/MY-GITHUB-ORG/MY-REPO-NAME) for details.

## ID Ranges

These are stored in the file

 * [foobar-idranges.owl](foobar-idranges.owl)

** ONLY USE IDs WITHIN YOUR RANGE!! **

If you have only just set up this repository, modify the idranges file
	and add yourself or other editors. Note Protege does not read the file
- it is up to you to ensure correct Protege configuration.


### Setting ID ranges in Protege

We aim to put this up on the technical docs for OBO on http://obofoundry.org/

For now, consult the [GO Tutorial on configuring Protege](http://go-protege-tutorial.readthedocs.io/en/latest/Entities.html#new-entities)

## Imports

All import modules are in the [imports/](imports/) folder.

There are two ways to include new classes in an import module

 1. Reference an external ontology class in the edit ontology. In Protege: "add new entity", then paste in the PURL
 2. Add to the imports/foo_terms.txt file

After doing this, you can run

`./run.sh make all_imports`

to regenerate imports.

Note: the foo_terms.txt file may include 'starter' classes seeded from
the ontology starter kit. It is safe to remove these.

## Design patterns

You can automate (class) term generation from design patterns by placing DOSDP
yaml file and tsv files under src/patterns. Any pair of files in this
folder that share a name (apart from the extension) are assumed to be
a DOSDP design pattern and a corresponding tsv specifying terms to
add.

Design patterns can be used to maintain and generate complete terms
(names, definitions, synonyms etc) or to generate logical axioms
only, with other axioms being maintained in editors file.  This can be
specified on a per-term basis in the TSV file.

Design pattern docs are checked for validity via Travis, but can be
tested locally using

`./run.sh make patterns`

In addition to running standard tests, this command generates an owl
file (`src/patterns/pattern.owl`), which demonstrates the relationships
between design patterns.

To compile design patterns to terms run:

`./run.sh make definitions.owl`

This generates a file (`src/patterns/definitions.owl`) which is
imported into the editors file.


## Release Manager notes

You should only attempt to make a release AFTER the edit version is
committed and pushed, and the travis build passes.

These instructions assume you have
[docker](https://www.docker.com/get-docker). This folder has a script
[run.sh](run.sh) that wraps docker commands.

to release:

    cd src/ontology
    ./run.sh make

If this looks good type:

    ./run.sh make prepare_release

This generates derived files such as foobar.owl and foobar.obo and places
them in the top level (../..). The versionIRI will be added.

Commit and push these files.

    git commit -a

And type a brief description of the release in the editor window

Finally type

    git push origin master

IMMEDIATELY AFTERWARDS (do *not* make further modifications) go here:

 * https://github.com/MY-GITHUB-ORG/MY-REPO-NAME/releases
 * https://github.com/MY-GITHUB-ORG/MY-REPO-NAME/releases/new

The value of the "Tag version" field MUST be

    vYYYY-MM-DD

The initial lowercase "v" is REQUIRED. The YYYY-MM-DD *must* match
what is in the versionIRI of the derived foobar.owl (data-version in
foobar.obo).

Release title should be YYYY-MM-DD, optionally followed by a title (e.g. "january release")

Then click "publish release"

__IMPORTANT__: NO MORE THAN ONE RELEASE PER DAY.

The PURLs are already configured to pull from github. This means that
BOTH ontology purls and versioned ontology purls will resolve to the
correct ontologies. Try it!

 * http://purl.obolibrary.org/obo/foobar.owl <-- current ontology PURL
 * http://purl.obolibrary.org/obo/foobar/releases/YYYY-MM-DD.owl <-- change to the release you just made

For questions on this contact Chris Mungall or email obo-admin AT obofoundry.org

# Travis Continuous Integration System

Check the build status here: [![Build Status](https://travis-ci.org/MY-GITHUB-ORG/MY-REPO-NAME.svg?branch=master)](https://travis-ci.org/MY-GITHUB-ORG/MY-REPO-NAME)

Note: if you have only just created this project you will need to authorize travis for this repo.

 1. Go to [https://travis-ci.org/profile/MY-GITHUB-ORG](https://travis-ci.org/profile/MY-GITHUB-ORG)
 2. click the "Sync account" button
 3. Click the tick symbol next to MY-REPO-NAME

Travis builds should now be activated

