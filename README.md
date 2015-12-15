# ontology-starter-kit

Initialize a GitHub repo for managing your ontology the OBO Library way!

# Requirements

Any Linux or OS X command line environment should work. You will minimally need the following installed:

 * perl
 * git

The kit will also try to make an initial ontology release, unless you tell it not to. For this you will need:

 * robot
 * owltools

On the command line

# Protocol

## Download this starter package

It's recommended you get a release version

## Initialize

First you must be in the root level of the starter kit

    cd ontology-starter-kit

The `seed-my-ontology-repo.pl` command does everything you need. For help:

    ./seed-my-ontology-repo.pl  -h

An example:

    ./seed-my-ontology-repo.pl  -d chebi -d ro -u obophenotype -t "ontology-of-foos-and-bars" foobaro

This will create your starter files in `target/ontology-of-foos-and-bars`

## Push to GitHub

The starter kit will automatically initialize a git project, add all files and commit.

You will need to create a project on GitHub. For example `obophenotype/ontology-of-foos-and-bars`

Follow the instructions there. E.g.

```
cd target/ontology-of-foos-and-bars
```

Note: you can now mv `target/ontology-of-foos-and-bars` to anywhere you like in your home directory. Or you can do a fresh checkout from github

## OBO Library metadata

You can create pull requests for your ontology on the OBO Foundry. See the `src/metadata` file for more details.

## Additional

You will want to also:

 * enable travis
 * enable zenodo (optional)

## More documentation

You will find additional documentation in the src/ontology/README-editors.md file in your repo
