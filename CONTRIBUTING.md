# Instructions for DEVELOPERs of ODK

This is intended for developers only, see [README](README.md) for the
main docs.

## Development principles

### Project’s aims

The primary aim of the ODK (its mission statement, if you will) is to
make it possible for any ontology project to benefit from thoroughly
designed, well tested ontology engineering workflows, even if the
project does not have the luxury of a full-time ontology pipeline
engineer always available to fix snafus and keep things running.

From this aim, we derive the following guidelines that developers should
keep in mind whenever working on the ODK (especially when adding new
features):

(1) No feature should require from the user to install anything on their
machine beyond Docker (required to run the ODK images) and Git (needed
to work on ODK repositories).

(2) As much as possible, features should not require any specialised
configuration beyond what can be configured in the `*-odk.yaml` ODK
configuration file.

(3) All standard workflows should be usable by people that do not have
engineering or programming skills beyond the ability of running simple
commands on the command line.

(4) Point (3) applies to updating an existing ODK-managed project to a
newer version of the ODK, which should not require the intervention of an
engineer.

### Custom/advanced workflows

For the projects that do have the luxury of an ontology pipeline
engineer, the ODK must not stand in the way of any custom or advanced
workflow that might be necessary.

An ontology pipeline engineer must always be able to customise any
standard ODK workflow and to add specialised workflows as needed.

However, whenever custom workflows are used, the promise of smooth
updates (point 4 in the previous section) no longer holds — it is
explicitly acceptable for ODK developers to introduce changes that may
break custom workflows.

### Technological stack and dependencies

#### Docker

Currently, the ODK is provided as a Docker image. While it would be
desirable _not_ to depend on Docker, this is not realistically feasible
for now.

Still, as much as possible, developers should refrain from assuming that
the Docker image will always be used. For example, workflows should not
invoke a tool by hardcoding its path within the Docker image, but
instead assume the tool is available in the _PATH_ (so, for example,
ROBOT should be invoked simply as `robot`, _not_ as `/tools/robot`).

#### Git

Currently, the ODK assumes that an ontology project will be
version-controlled using Git.

There is no plan to support other version control systems (such as
Mercurial, Subversion, etc.), and it is fine for developers to continue
assuming the use of Git.

#### GitHub

Several features in the ODK assumes that an ontology project is or will
be hosted on GitHub.

This is only fine as long as those features are not *required*. It
must *always* be possible to host a ODK-managed ontology on any other
Git hosting service (including self-hosting).

#### POSIX compatibility and “GNU-isms”

The ODK image is built on top of a GNU/Linux system, and there is no
plan to change that anytime soon. However, as much as possible, even for
processes that are intended to run within a ODK container it is best to
avoid relying on GNU-specific behaviours or options (so-called
“GNU-isms”), unless doing so provides a clear benefit (e.g. in
performance or readability) over a strictly POSIX-compliant alternative.

That rule applies more strongly to wrapper scripts that are intended to
be run from the host’s shell rather than from within the ODK container
(e.g. `run.sh`, `seed-via-docker.sh`): those scripts *must* avoid any
features specific to one particular flavour of the Bourne shell (be it
`bash`, `dash`, `zsh`, etc.).

The exception to that rule is for the standard ODK-generated Makefile:
it is explicitly fine for that Makefile to depend on features that are
specific to GNU Make.

#### Operating systems and architectures.

The ODK should be usable at least on:

* GNU/Linux (any distribution, x86\_64 only);
* macOS X (any version >= 10.12, x86\_64 and arm64);
* Windows (versions 10 and 11, 86\_64 only).

Running on other systems, versions, or architectures may be possible but
is not officially supported.

## Templating system

Creating (“seeding”) a ODK-managed repository is done with the
[odk/odk.py](odk/odk.py) script (available, within the ODK image, as
`/tools/odk.py`). The `seed` command of that script instantiates the
Jinja2 templates found in the [template/](template) directory
(`/tools/templates` within the ODK image).

For example, the file
[template/src/ontology/Makefile.jinja2](template/src/ontology/Makefile.jinja2)
will compile to a file `src/ontology/Makefile` in the target/output
directory.

Jinja2 templates should be fairly easy to grok for anyone familiar with
templating systems. We feed the template engine with a project object
that is passed in by the user (see below).

Logic in the templates should be kept to a minimum (though the
aforementioned `Makefile.jinja2` template is a great offender of this
principle). Whenever possible, complex logic should reside in the
`odk.py` script, which should provide ready-to-use variables and lists
for the templates to exploit.

Templates may contain Jinja2 comments (`{# .. #}`) which are intended
for ODK *developers* only (as those comments will not appear in the
produced files). Templates may also contain comments intended for the
*users*, using whatever comment syntax is appropriate for the kind of
produced file (e.g. a Makefile template may contain comments as lines
starting with `#`, a RDF/XML template may contain comments as
`<!-- ... -->` blocks, etc).

### Dynamic File Names

Sometimes the odk needs to create a file whose name is based on an
input setting or configuration; sometimes lists of such files need to
be created.

For example, if the user specifies 3 external ontology dependencies,
then we want to see the repo with 3 files `imports/{{ont.id}}_import.owl`

Rather than embed this logic in code, we can use special “dynamic”
templates (identified by a name starting with `_dynamic`). A dynamic
template is a “tar-like” bundle containing an arbitrary number of files,
each file starting with a line of the form:

```
^^^ path/to/file
```

where `path/to/file` is the complete pathname of the file to create. All
subsequent lines in the bundle, up to the next `^^^` line, will end up
in that file.

Because the entire bundle is itself a Jinja2 template, and the bundle is
extracted _after_ template expansion, this system allows us to have

(1) dynamic file names:

```
^^^ src/ontology/{{ project.id }}-idranges.owl
# ID ranges file
@Prefix: rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
...
```

(2) files that are created or not depending on the value of a
configuration option:

```
{% if project.use_templates %}
^^^ src/templates/README.md
# ROBOT templates
...
{%- endif %}
```

(3) and files that are created serially in a Jinja2 loop:

```
{% for imp in project.import_group.products %}
^^^ src/ontology/imports/{{ imp.id }}_import.owl
...
```

## The Project object

Currently the datamodel is specified as python dataclasses, for now
the best way to see the complete spec is to look at the classes
annotated with `@dataclass` in the code.

There is a [schema](schema) folder but this is incomplete as the
dataclasses-scheme module doesn't appear to work (TODO)...

An auto-generated documentation is available in
[docs/project-schema.md](docs/project-schema.md). That documentation is
updated by running `make docs` from the top-level directory. Additional
documentation should at some point be available in
[docs/schema-options.md](docs/schema-options.md).

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
  update           Updates a pre-existing repository.
```

The most common command is `seed`.

## Building the ODK

### Setting up a new machine for ODK development

ODK development can be done on any system supported by the ODK
(GNU/Linux, macOS, Windows). You need:

* a working Docker installation (on macOS and Windows, all you need is
  to install Docker Desktop; on GNU/Linux, refer to the package manager
  of your distribution, or install from source);
* the Git version control system;
* the Make build tool.

### Making a local build

To build an image to use on your local system, run from the top-level
directory:

```sh
$ make build
```

This will build both the `odklite` and `odkfull` images, and make them
available in your local Docker registry. Note that this means that any
subsequent invocation of `obolibrary/odkfull:latest` (or simply
`obolibrary/odkfull`) will use the newly built version, _not_ the latest
published version available on the Docker Hub library.

To test:

```sh
$ make tests
```

These will seed a few example repos in the target/ folder, some from
command line opts, others from a project.yaml.

These are pseudo-tests as the output is not examined, however they do
serve to guard against multiple kinds of errors as the seed script
will often fail if things are not set up correctly.

<a id="publishing-images" />

### Building for publication

Compared to a build solely intended for local use (previous section),
building images intended for publication on the Docker Hub library
requires some additional steps.

#### Setup

1. You must make sure your local Docker installation is logged in to
   your Docker Hub account:

```sh
$ docker login
```

Your Docker account must have access rights to the `obolibrary`
organisation.

2. You must be equipped to build “multi-arch” images, that can be used
   on more architectures than the your current system’s architecture.

To build multi-arch images, you need to have
[buildx](https://github.com/docker/buildx) enabled on your Docker
installation. On MacOS with Docker Desktop, `buildx` should already be
enabled. For other systems, refer to Docker's documentation.

Create a *builder* instance for multi-arch builds:

```sh
$ docker buildx create --name multiarch --driver docker-container --use
```

Those setup steps normally only need to be done *once*, prior to do your
first ever build for publication. However, should you need to reset your
multiarch builder, this can be done with:

```sh
$ docker buildx rm multiarch
$ docker buildx create --name multiarch --driver docker-container --use
```

#### Building and publishing

If the preliminary steps in the previous section have been performed,
you can then build and push multi-arch images by running:

```sh
$ make publish-multiarch
```

Use the variable `PLATFORMS` to specify the architectures for which an
image should be built. The default is `linux/amd64,linux/arm64`, for
images that work on both x86_64 and arm64 machines.

Should you want to publish the multi-arch images under the `obotools`
organisation rather than `obolibrary` (we sometimes do that to test some
particularly big changes that we do not want to publish in the normal
`obolibrary` organisation), you need to run instead:

```sh
$ make publish-multiarch IM=obotools/odkfull IMLITE=obotools/odklite DEV=obotools/odkdev
```  

## General SOP for ODK release and publication

There are three types of releases: major, minor and development snapshot.
  - Major versions include changes to the workflow system.
  - Minor versions include changes to tools, such as ROBOT or Python
    dependencies.
  - Development snapshots reflect the current state of the `main`
    (`master`) branch.

They all have slightly different procedures which we will detail below.

### Major releases

Major releases contain changes to the workflow system of the ODK, e.g.
changes to the `Makefile` and various supporting scripts such as
`run.sh`. They require users to update their repository with `sh run.sh
update_repo`.

Major releases are typically incremented (a bit confusingly) on the
"minor" version number of ODK, i.e. 1.4, 1.5, 1.6 etc.  There are
currently (2024) no plans to increment on the major version - this will
likely be reserved to fundamental changes like switching from `make` to
another workflow system or dropping `docker` (both are unlikely to
happen in the midterm).

There should be no more than 2 such version updates per year (ideally
1), to reduce the burden on users to maintain their repositories.

#### SOP for creating a major release

* Put the `master` branch in the state we want for release (i.e. merge
  any approved PR that we want included in that release, etc.).
* Ensure your local `master` branch is up-to-date (`git pull`) and run a
  basic build (`make build tests`). This _should_ not result in any
  surprises as this exact command is run every time we merge a change into
  the `master` branch by our CI system. However, as various dependencies
  of the system are still variable (in particular unix package versions),
  there are occasionally situations where the build fails or, less likely,
  the subsequent tests.
* Do any amount of testing as needed to be confident we are ready for
  release. For major releases, it makes sense to test the ODK on at
  least 10 ontologies. In 2024 we typically test:
  * All ontologies we test for _minor_ releases (see below);
  * FlyBase ontologies
    ([fbbt](https://github.com/FlyBase/drosophila-anatomy-developmental-ontology),
    [fbcv](https://github.com/FlyBase/drosophila-developmental-ontology),
    [dpo](https://github.com/FlyBase/drosophila-phenotype-ontology));
  * [NCBITaxon](https://github.com/obophenotype/ncbitaxon);
  * [Zebrafish Phenotype
    Ontology](https://github.com/obophenotype/zebrafish-phenotype-ontology)
    (should only be done in collaboration with a ZP core developer, too many
    points of failure);
* We suggest to have at least 1 other ODK core team member run 3 release
  pipelines to reduce the risk of operating system related differences.
* Build and publish the images as explained in the [corresponding
  section](#publishing-images).
* As soon as the Docker images are published, create and publish a
  GitHub release (check last major release on how to format correctly).
* After the release is _published_, create a new PR updating the
  `VERSION = "v1.X"` variable in the `Makefile` to the next major
  version number.

### Minor releases

Minor releases are normally releases that contain only changes about the
_tools_ provided by the ODK, and no changes about the _workflows_. As
such, they do not require users to update their repositories. All users
need to do to start using a new minor release is to pull the latest
Docker image of the ODK (`pull obolibrary/odkfull:latest`).

Minor releases are only provided for the current major branch of the
ODK. For example, if the latest major release is v1.5, we will provide
(as needed) minor releases v1.5.1, v1.5.2, etc, but we will _not_
provide minor releases for any version prior to 1.5; once v1.6 is
released, we will likewise stop providing v1.5.x minor releases. In
other words, only one major branch is actively supported at any time.

#### SOP for creating a minor release

* As soon as a major branch (v1.X) has been released, create a
  `BRANCH-1.X-MAINTENANCE` branch forked from the `v1.X` release tag.
* As development of the next major branch (v1.X+1) is ongoing, routinely
  backport tools-related changes to the `BRANCH-1.X-MAINTENANCE` branch.
* By convention, changes to the next major branch that are introduced by
  a PR tagged with a `hotfix` label should also be backported to the
  maintenance branch.
* To avoid cluttering the maintenance branch with multiple “Python
  constraints update” backport commits, it is recommended to backport
  all Python constraints at once, shortly before a minor release.
* There are no strict guidelines about when a minor release should
  happen. The availability of a new version of ROBOT is usually reason
  enough to make such a release, but upgrades to other tools can also
  occasionally justify a minor release.

Once the decision to make a minor release has been made:

* Make sure all tools-related updates (including Python tools) have been
  backported.

* Do any amount of testing as needed to be confident we are ready for
  release. For minor releases, it makes sense to test the ODK on at
  least 5 ontologies. In 2024 we typically test:
  - [Mondo](https://github.com/monarch-initiative/mondo)
    ([docs](https://mondo.readthedocs.io/en/latest/developer-guide/release/))
    (a lot of use of old tools, like owltools, interleaved with ROBOT, heavy
    dependencies on serialisations, perl scripts);
  - [Mondo Ingest](https://github.com/monarch-initiative/mondo-ingest)
    (a lot of use of sssom-py and OAK, interleaved with heavyweight
    ROBOT pipelines);
  - [Uberon](https://github.com/obophenotype/uberon) (ROBOT plugins, old
    tools like owltools);
  - [Human Phenotype
    Ontology](https://github.com/obophenotype/human-phenotype-ontology)
    (uses of ontology translation system (babelon), otherwise pretty
    standard ODK, high impact ontology);
  - [Cell Ontology](https://github.com/obophenotype/cell-ontology) (relatively standard, high impact ODK setup).
* Update the CHANGELOG.md file.
* Bump the version number to `v1.X.Y` in
  - the top-level `Makefile`,
  - the `Makefile` in the `docker/odklite` directory.
* If the minor release includes a newer version of ROBOT, and if that
  has not already been done when ROBOT itself was updated, update the
  version number in `docker/robot/Makefile` so it matches the version of
  ROBOT that is used.
* Push all last-minute changes (CHANGELOG and version number updates) to
  the `BRANCH-1.X-MAINTENANCE` branch.
* Build and publish the images from the top of the
  `BRANCH-1.X-MAINTENANCE` branch as explained in the [corresponding
  section](#publishing-images).
* Create a GitHub release from the tip of the `BRANCH-1.X-MAINTENANCE`
  branch, with a `v1.X.Y` tag.
* Resume backporting changes to the `BRANCH-1.X-MAINTENANCE` until the
  time comes for the next minor release.

### Development snapshot

Development snapshots reflect the current state of the main (`master`)
branch. They do not undergo the same level of testing (or any testing at
all) as the normal releases, and are intended to help trialing and
debugging the changes that happen in the `master` branch.

Development snapshots should _not_ be used in a production environment.
Feel free to use them if you want to help us developing the next major
release, but if you use them in your production pipelines, understand
that you’re doing so at your own risk.

Development snapshots are tagged with the `dev` tag on docker, and with
the `-dev` suffix in the `Makefile` pipeline (e.g. `v1.6-dev` to
indicate that this is a snapshot of the ODK on the way towards a 1.6
release). Development snapshots can happen any time, but typically
happen once every 1 to 4 weeks.

#### SOP for creating a development snapshot

* Put the `master` branch in the state we want for release (i.e. merge
  any approved PR that we want included in that release, etc.).
* Ensure your local `master` branch is up-to-date (`git pull`) and run a
  basic build (`make build tests`) (see comments in Major release
  section for details about the rationale).
* We do not typically do any additional testing for the development
  snapshot.
* Build and publish the images as explained in the [corresponding
  section](#publishing-images), *but* using `make publish-multiarch-dev`
  instead of `make publish-multiarch`.
* Do NOT create a GitHub release!
* Your build has been successful when the `dev` image appears as updated
  [on Dockerhub](https://hub.docker.com/r/obolibrary/odkfull/tags).

## Pull request rules

1. All changes must be introduced through a PR (no commit directly to
   the `master` branch).
2. One PR per feature. However, when a PR touches a particular area of
   the code, it is fine to include unrelated refactoring of that code in
   the PR, as long as the refactoring happens in separate commit(s).
3. Complex changes must be broken down in separate commits, each commit
   implementing a single logical change.
4. Each commit must have a proper commit message that describes what the
   change is about.

Contributors submitting PRs that do not follow those rules may be asked
to re-submit a correct PR, even if the changes introduced by the PR are
otherwise approved.

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

If the component needs to be built from source, do so in [the Dockerfile for odkbuild](docker/builder/Dockerfile), 
and install the compiled file(s) in either the `/staging/full` tree or the `/staging/lite` tree, for
inclusion in `odkfull` or `odklite` respectively.

If the component is a Python package, add it to the `requirements.txt.full`
file, and *also* in the `requirements.txt.lite` file if it is to be part
of `odklite`. Please try to avoid version constraints unless you can
explain why you need one.

Python packages are "frozen" so that any subsequent build of the ODK
will always include the exact same version of every single package. To
update the frozen list, run `make constraints.txt` in the top-level
directory. This should be done at least (1) whenever a new package is
added to `requirements.txt.full`, (2) whenever the base image is
updated. It can also be done at any time during the development cycle to
ensure that we pick regular updates of any package we use.

## Tools to update

The following table lists all tools that should be checked for updates
whenever a new release is in preparation.

| Tool | Where to check for updates | Notes |
| ---- | -------------------------- | ----- |
| ROBOT | https://github.com/ontodev/robot/releases | |
| ROBOT KGCL Plugin | https://github.com/gouttegd/kgcl-java/releases | |
| ROBOT ODK Plugin | https://github.com/INCATools/odk-robot-plugin/releases | |
| ROBOT SSSOM Plugin | https://github.com/gouttegd/sssom-java/releases | |
| DOSDP-Tools | https://github.com/INCATools/dosdp-tools/releases | |
| Relation-Graph | https://github.com/balhoff/relation-graph/releases | |
| Dicer | https://github.com/gouttegd/dicer/releases | |
| Soufflé | https://github.com/souffle-lang/souffle/releases | |
| Fastobo-validator | https://github.com/fastobo/fastobo-validator/releases | |
| RDFTab | https://github.com/ontodev/rdftab.rs/releases | |
| Konclude | https://github.com/konclude/Konclude/releases | unlikely to get a new release |
| OWLTools | https://github.com/owlcollab/owltools/releases | unlikely to get a new release |
| Jena | https://jena.apache.org/download/ | |
| Ammonite | https://github.com/lihaoyi/Ammonite/releases | to be removed in ODK 1.7 (replaced by Scala-CLI) |
| Scala-CLI | https://github.com/VirtusLab/scala-cli/releases | |

Python packages (e.g. the Ontology Access Kit aka `oaklib`) should be
automatically updated to their latest version whenever Python
constraints are updated with `make constraints.txt` as explained in the
previous section.
