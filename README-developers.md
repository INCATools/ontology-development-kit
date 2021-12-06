# Instructions for DEVELOPERs of ODK

This is intended for developers only, see [README](README.md) for the
main docs.

## Installation

For running locally without Docker you will need

 * robot
 * owltools
 * python3.6 or higher

See [Dockerfile](Dockerfile) for details on how to obtain these

## How it works

Previously ODK used a perl script to create a new repo. This iterated
the [template/](template) directory and used special magic for expanding into a
target folder. This has been replaced by python code
[odk/odk.py](odk/odk.py) with makes used of Jinja2 templates.

For example, the file
[template/src/ontology/Makefile.jinja2](template/src/ontology/Makefile.jinja2)
will compile to a file `src/ontology/Makefile` in the target/output
directory.

Jinja2 templates should be fairly easy to grok for anyone familiar
with templating systems. The syntax is very similar to Liquid
templates, which are used extensively on the OBO site. We feed the
template engine with a project object that is passed in by the user
(more on that later).

Logic in the templates should be non-existent.

## Dynamic File Names

Sometimes the odk needs to create a file whose name is based on an
input setting or configuration; sometimes lists of such files need to
be created.

For example, if the user specifies 3 external ontology dependencies,
then we want to see the repo with 3 files `imports/{{ont.id}}_import.owl`

Rather than embed this logic in code, we include all dynamic files in
a single "tar-esque" formated file: [template/_dynamic_files.jinja2](template/_dynamic_files.jinja2)

This file is actually a specification for multiple files, each target
file specified with `^^^`. Because the parent file is interpreted
using templates, we can have dynamic file names, and entire files
created via looping constructs.

## The Project object

Currently the datamodel is specified as python dataclasses, for now
the best way to see the complete spec is to look at the classes
annotated with `@dataclass` in the code.

There is a [schema](schema) folder but this is incomplete as the
dataclasses-scheme module doesn't appear to work (TODO)...

There are also example `project.yaml` files in the
[examples](examples) folder, and these also serve as rudimentary unit
tests.

See for example [examples/go-mini/project.yaml](examples/go-mini/project.yaml)

The basic data model is:

 * An `OntologyProject` consists of various configuration settings, plus `ProductGroup`s
 * These are:
    * An `ImportProduct` group which specifies how import files are generated
    * A `SubsetProduct` group which specifies how subset/slim files are generated
    * Other product groups for reports and templates

Many ontology projects need only specify a very minimal configuration:
id of ontology, github/gitlab location, and list of ontology ids for
imports. However, for projects that need to customize there are
multiple options. E.g. for an import product you can optionally
specific a particular URL that overrides the default PURL.

Note that for backwards compatibility, a project.yaml file is not
required. A user can specify an entire repo by running `seed` with
options such as `-d` for dependencies.

Note that in all cases a `project.yaml` file is generated.

## ODK commands

```
$ ./odk/odk.py --help
Usage: odk.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-dynfile   For testing purposes
  create-makefile  For testing purposes
  dump-schema      Dumps the python schema as json schema.
  export-project   For testing purposes
  seed             Seeds an ontology project
```

The most common command is seed.

## Updating a Makefile and/or repo

Previously with odk there was no path to either upgrading an existing
project with new settings (i.e. adding an import) OR to take advantage
of changes to the odk (e.g changes in the core Makefile).

This should now be easier with the new odk, although the
implementation emphasis has been on the seed command. Some things that
will make this easier:

 * Convention of using a second loaded Makefile for custom changes
 * Maintaining a project.yaml in root folder will allow easy regeneration

TODO: add a refresh command. This could run odk *in place*, but
preserving protected files. TBD how to determine protected
files. Obviously the edit file should not be touched. Could use git
log to determine if any modifications have been made?

## General SOP for ODK release and publication

* Put the `master` branch in the state we want for release (i.e. merge any approved PR that we want included in that release, etc.).
* Update the [constraits.txt file](https://github.com/INCATools/ontology-development-kit/pull/476#issuecomment-924050937)
* Do any amount of testing as needed to be confident we are ready for release (at the very least, do a local build with `make build` and run the test suite with `make tests`; possibly run some mock releases on known ontologies such as `FBbt`, etc.).
* Tag the release and push the tag to GitHub and create a formal release from the newly pushed tag.
* Run `docker login` to ensure you are logged in. You must have access rights to `obolibrary` organisation to run the following.
* Run `make publish-multiarch` to publish the ODK in the `obolibrary` dockerhub organisation.

If you want publish the multi-arch images under the `obotools/` organisation, you need to run locally:

```sh
$ docker buildx create --name multiarch --driver docker-container --use
$ make publish-multiarch IM=obotools/odkfull IMLITE=obotools/odklite DEV=obotools/odkdev
```

The first command only being needed when you attempt a multi-arch build for the first time. Its effects are persistent, so it will never be needed again for any subsequent release — unless you completely reset your Docker installation in the meantime.

More details below.

## Docker

Note that with v1.2 the main odkfull [Dockerfile](Dockerfile) is at
the root level. We now use a base alpine image for compactness, and
selectively add in unix tools like make and rsync.

Note also that we include odk.py and the template folders in the
image. This means that odk seed can now be run from anywhere!

To build the Docker image from the top level:

```
make build
```

Note that this means local invocations to use `obolibrary/odkfull`
will use the version you built.

To test:

```
make tests
```

To publish on Dockerhub:

```
make publish
```

### Multi-arch images

To build multi-arch images that will work seemleassly on several
platforms, you need to have [buildx](https://github.com/docker/buildx)
enabled on your Docker installation. On MacOS with Docker Desktop,
`buildx` should already be enabled. For other systems, refer to Docker's
documentation.

Create a *builder* instance for multi-arch builds (this only needs to be
done once):

```
docker buildx create --name multiarch --driver docker-container --use
```

You can then build and push multi-arch images by running:

```
make publish-multiarch
```

Use the variable `PLATFORMS` to specify the architectures for which an
image should be built. The default is `linux/amd64,linux/arm64`, for
images that work on both x86_64 and arm64 machines.

## Some notes on templating and logic

There is a potential for some confusion as to responsibility for
logic. On the one hand we have dependency logic in the Makefile. But
we also have minimal logic in deciding what to put in the Makefile.

For example, we could move some logic from the Makefile by using
for/endfor Jinja constructs and unfolding every product in a group and
have an explicit non-pattern target in the Makefile. Or we can
continue to write targets with patterns. Or we can do a mixture of
both.

Additionally there is some minimal logic in the python odk code, but
this is kept to an absolute minimum; the role of the python code is to
run template expansions.

In general the decision is to keep the templating as simple as
possible, which leads to a slight mixed two level system.

One gotcha is the two levels of comments. The `{# .. #}` comments are
template comments for the eyes of developers only. These are ignored
when compiling down to the target file. Then we also have Makefile
comments `#` which remain in the target file, and are intended for
advanced ontology maintainers who need to debug their workflows. These
are intermingled in Makefile.jinja2

## Unit Tests

To run:

```
make test
```

These will seed a few example repos in the target/ folder, some from command line opts, others from a project.yaml

These are pseudo-tests as the output is not examined, however they do
serve to guard against multiple kinds of errors as the seed script
will often fail if things are not set up correctly.

The examples folder serves for both unit test and documentation purposes.

## Migration System

TODO


## Adding new programs or Python modules to the ODK

How and where to add a component to the ODK depends on the nature of the
component and whether it is to be added to `odkfull` or `odklite`.

As a general rule, new components should probably be added to `odkfull`,
as `odklite` is intended to be kept small. Components should only be
added to `odklite` if they are required in rules from the ODK-generated
standard Makefile. Note that any component added to `odklite` will
automatically be part of `odkfull`.

Is the component available as a standard Ubuntu package? Then add it to
the list of packages in the `apt-get install` invocation in [the main
Dockerfile](Dockerfile) (for inclusion into `odkfull`) or in [the
Dockerfile for odklite](docker/odklite/Dockerfile).

Is the component available as a pre-built binary? Be careful that many
projets only provide pre-built binaries for the x86 architecture. Using
such a binary would result in the component being unusable in the arm64
version of the ODK (notably used on Apple computers equipped with M1
CPUs, aka "Apple Silicon").

Java programs available as pre-built jars can be installed by adding new
`RUN` commands at the end of either the main Dockerfile (for `odkfull`)
or the Dockerfile for `odklite`.

If the component needs to be built from source, do so in [the Dockerfile
for odkbuild](docker/build/Dockerfile), and install the compiled file(s)
in either the `/staging/full` tree or the `/staging/lite` tree, for
inclusion in `odkfull` or `odklite` respectively.

If the component is a Python package, adds it to the `requirements.txt`
file, and *also* in the `requirements.txt.lite` file if it is to be part
of `odklite`. Please try to avoid version constraints unless you can
explain why you need one.

Python packages are "frozen" before a release by installing all the
packages listed in `requirements.txt` into a virtual environment and
running `python -m pip freeze > constraints.txt` from within that
environment.
