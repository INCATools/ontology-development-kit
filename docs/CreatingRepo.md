# Creating a Repository

This is instructions on how to create an ontology repository in
GitHub. This will only need to be done once per project. You may need
assistance from someone with basic unix knowledge in following
instructions here.

We will walk you though the steps to make a new ontology project

## 1. Install and Start Docker

 * [docker](https://www.docker.com/get-docker)

See the README on the [ODK site](https://github.com/INCATools/ontology-development-kit) for instructions on how to do this without Docker.

## 2. Download the wrapper script and pull latest ODK version

 * Linux/Mac: [seed-via-docker.sh](https://raw.githubusercontent.com/INCATools/ontology-development-kit/master/seed-via-docker.sh)
 * PC: [seed-via-docker.bat](https://raw.githubusercontent.com/INCATools/ontology-development-kit/master/seed-via-docker.bat)
 * First, make sure you have Docker running (you will see the Docker whale in your toolbar on a Mac)
 * To make sure you have the latest version of the ODK installed, run in the command line 

    `docker pull obolibrary/odkfull`

**NOTE** The very first time you run this it may be slow, while docker downloads necessary images. Don't worry, subsequent runs should be much faster!

## 3. Run the wrapper script

You can either pass in a `project.yaml` file that specifies your ontology project setup, or you can pass arguments on the command line.

Passing arguments on the command line:

    ./seed-via-docker.sh -d po -d ro -d pato -u cmungall -t "Triffid Behavior ontology" triffo

Using a the predefined [examples/triffo/project.yaml](examples/triffo/project.yaml) file:

    ./seed-via-docker.sh -C examples/triffo/project.yaml

You can add a -c (lowercase) just before the -C (capital c) in the command to first delete any previous attempt to generate your ontology with the ODK, and then replaces it with a completely new one.

This will create your starter files in
`target/triffid-behavior-ontology`. It will also prepare an initial
release and initialize a local repository (not yet pushed to your Git host site such as GitHub or GitLab).

You can customize at this stage, or (recommended) after making an initial push to your git host.

## 4. Push to Git hosting website

The development kit will automatically initialize a git project, add all files and commit.

You will need to create a project on you Git hosting site.

*For GitHub:*

 1. Go to: https://github.com/new
 2. The owner MUST be the org you selected with the `-u` option. The name MUST be the one you set with `-t`.
 3. Do not initialize with a README (you already have one)
 4. Click Create
 5. See the section under "…or push an existing repository from the command line"

*For GitLab:*

 1. Go to: https://gitlab.com/projects/new
 2. The owner MUST be the org you selected with the `-u` option. The name MUST be the one you set with `-t`.
 3. Do not initialize with a README (you already have one)
 4. Click 'Create project'
 5. See the section under "Push an existing Git repository"

Follow the instructions there. E.g.

```
cd target/triffid-behavior-ontology
git remote add origin git@github.com:cmungall/triffid-behavior-ontology.git
git push -u origin master
```

Note: you can now mv `target/triffid-behavior-ontology` to anywhere you like in your home directory. Or you can do a fresh checkout from github.


## Next Steps: Edit and release cycle

In your repo you will see a README-editors.md file that has been customized for your project. Follow these instructions.

Generally the cycle is to:

 - branch
 - edit the edit.owl file
 - make test
 - git commit
 - git push

To make a release:

`make prepare_release`

Note that any make step can be preceded by run.sh if you have Docker installed:

`sh run.sh make prepare_release`

## OBO Library metadata

The assumption here is that you are ahdering to OBO principles and
want to eventually submit to OBO. Your repo will contain stub metadata
files to help you do this.

You can create pull requests for your ontology on the OBO Foundry. See the `src/metadata` file for more details.

For more documentation, see http://obofoundry.org

## Additional

You will want to also:

 * enable travis
 * enable zenodo (optional)

See the README-editors.md file that has been generated for your project.
