# ontology-starter-kit

Initialize a GitHub repo for managing your ontology the OBO Library way!

For more details, see this post:
https://douroucouli.wordpress.com/2015/12/16/creating-an-ontology-project-an-update/

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

This will create your starter files in
`target/ontology-of-foos-and-bars`. It will also prepare an initial
release and initialize a repository.

You can customize at this stage, or (recommended) after making an initial push to github

## Push to GitHub

The starter kit will automatically initialize a git project, add all files and commit.

You will need to create a project on GitHub.

 1. Go to: https://github.com/new
 2. The owner MUST be the org you selected with the `-u` option. The MUST be the one you set with `-t`.
 3. Do not initialize with a README (you already have one)
 4. Click Create
 5. See the section under "…or push an existing repository from the command line"

Follow the instructions there. E.g.

```
cd target/ontology-of-foos-and-bars
git remote add origin git@github.com:obophenotype/foobar.git
git push -u origin master
```

Note: you can now mv `target/ontology-of-foos-and-bars` to anywhere you like in your home directory. Or you can do a fresh checkout from github

## OBO Library metadata

You can create pull requests for your ontology on the OBO Foundry. See the `src/metadata` file for more details.

## Additional

You will want to also:

 * enable travis
 * enable zenodo (optional)

## Customizing

You will likely want to customize the build process, and of course to edit the ontology.

The main thing you will want to do is to modify the seeds that are
used to build the imports. The ones that are there are just examples,
edit them as you like. See the ROBOT docs and the [OBO
Tutorial](https://github.com/jamesaoverton/obo-tutorial) for more
info.


## More documentation

You will find additional documentation in the src/ontology/README-editors.md file in your repo
