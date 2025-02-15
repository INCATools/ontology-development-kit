# v1.6 (Planned)

For more detailed changes see:

- [Milestone definition](https://github.com/INCATools/ontology-development-kit/milestone/8)
- [All changes since the last major release](https://github.com/INCATools/ontology-development-kit/compare/v1.5...v1.6)

## Highlights (Read this!)

- TBD

## New and updated tooling

- New [ROBOT Version 1.9.6](https://github.com/ontodev/robot/releases/tag/v1.9.6). This came with a great number of updates and upgrades, see release notes.
- J2cli, a command-line tool to process Jinja2 templates, has been replaced by [Jinjanator](https://github.com/kpfleming/jinjanator). If your custom workflows invoke the `j2` tool, you will need to update them to use `jinjanate` instead.
- New program `dicer-cli` to manage the ID range file.
- Ammonite, the Scala interpreter, is no longer provided in the ODKLite image. If you need Ammonite, you must now use the ODKFull image. Be warned that Ammonite is slated for complete removal in a future ODK release, you should use Scala-CLI instead.
- The Scala-CLI Scala runner has been added to the ODKFull image.

## New configuration options

- TBD

## Makefile workflows

- The `$(ont)-idranges.owl` file is now checked for validity as part of the normal test suite [#211](https://github.com/INCATools/ontology-development-kit/issues/211).

## Runner and Infrastructure

- TBD

## Bugfixes

- Added back `class-count-by-prefix.sparql` ([#1030](https://github.com/INCATools/ontology-development-kit/issues/1030)).
- Disabled `table-reader` mkdocs plugin ([#1028](https://github.com/INCATools/ontology-development-kit/issues/1028)).
- SPARQL-based tests on the `-edit` file now also cover any component included in the ontology, as well as any pattern-derived contents ([#1154](https://github.com/INCATools/ontology-development-kit/issues/1154)).

# v1.5

For more detailed changes see:

- [Milestone definition](https://github.com/INCATools/ontology-development-kit/milestone/7)
- [All changes since the last major release](https://github.com/INCATools/ontology-development-kit/compare/v1.4...v1.5)

## Highlights (Read this!)

- All processes within the ODK container now **runs under the identity of an (unprivileged) user by default**. This fixes the issue of generated files being owned by the superuser, when the Docker daemon itself runs as the superuser (as is the case by default on most GNU/Linux systems). See [PR1](https://github.com/INCATools/ontology-development-kit/pull/769), [PR2](https://github.com/INCATools/ontology-development-kit/pull/900), [PR3](https://github.com/INCATools/ontology-development-kit/pull/905).
    - **Consequences:** Some workflows that require superuser rights may not work anymore as expected.
    - **Mitigation:** If you have a workflow that requires being run as a superuser (for example, if you need to install extra Debian/Ubuntu packages via `apt-get`), set the environment variable `ODK_USER_ID` to 0 when running that workflow or, to always run all workflows as a superuser (as was the case in previous ODK versions), set the configuration parameter `run_as_root` to `True` before updating your repository.
- Change the definition of **"base release"**. See [PR](https://github.com/INCATools/ontology-development-kit/pull/810).
    - **Consequence:** The base file now does not only contain the editors axioms in their raw form, but the axioms "as intended by the ontology developer", for example, including inferences. For the base-specification see [here](https://oboacademy.github.io/obook/reference/base-specification/).
    - **Mitigation:** If you want a release that corresponds exactly to the old base file, use `baselite` instead.
- Allow refreshing the mirrors (externally downloaded ontologies) under `IMP=false`. See [PR](https://github.com/INCATools/ontology-development-kit/pull/973).
    - **Consequence**: you now _cannot rely on `IMP=false` anymore_ if you want to avoid refreshing mirrors as well - you need to use `IMP=false MIR=false` instead!
- Make qc.yml ODK managed by default, so it is actually being updated along with the rest of the files. See [PR](https://github.com/INCATools/ontology-development-kit/pull/990).
    - **Consequence:** If you have overwritten that workflow with custom content, you have to follow the mitigation strategies.
    - **Mitigation:** (1) migrate the custom content to a differently named workflow or (2) deactivate syncning of that workflow manually by adding a `workflows` section to your ODK config.
- Generate `custom_reports` during release process [PR](https://github.com/INCATools/ontology-development-kit/pull/997).
    - **Consequence:** This means that all reports configured in ODK are automatically updated at release time, so you have more files need to review during a release. 
    - **Mitigation:** Add your reports to `.gitignore` or remove them from your ODK config.
- We added the "International Edition" as a release product, including an entire workflow system for managing translations using the [Babelon format](https://github.com/monarch-initiative/babelon). This feature is still under development, but works - feel free to reach out if you like to test it.

## New and updated tooling

- New [ROBOT Version 1.9.5](https://github.com/ontodev/robot/releases/tag/v1.9.5)
- A lot of [updated python tools](https://github.com/INCATools/ontology-development-kit/blob/master/constraints.txt), including [OAK (0.5.25)](https://github.com/INCATools/ontology-access-kit), [SSSOM tools](https://github.com/mapping-commons/sssom-py) (0.4.4), [LinkML](https://linkml.io/) (1.7.4) and [curies](https://github.com/cthoyt/curies) (0.7.7). 
- The [Babelon Toolkit](https://github.com/monarch-initiative/babelon) for managing multilingual ontologies has beed added as well.
- A full list of all available python tools and there vesions is available [here](https://github.com/INCATools/ontology-development-kit/blob/v1.5/constraints.txt)
- Added table-reader plugin for mkdocs [PR](https://github.com/INCATools/ontology-development-kit/pull/861)
- Added Perl module Business::ISBN. [PR](https://github.com/INCATools/ontology-development-kit/pull/886)
- Updated Apache Jena, Soufflé, Fastobo-validator, Ammonite
- Added SSSOM-Java ([PR](https://github.com/INCATools/ontology-development-kit/pull/958)) and KGCL-Java ([PR](https://github.com/INCATools/ontology-development-kit/pull/995)) to `odkfull`.

## New configuration options

- Add option to include defined-by annotation in imports [PR](https://github.com/INCATools/ontology-development-kit/pull/929)
- Add option `release_annotate_inferred_axioms` [PR](https://github.com/INCATools/ontology-development-kit/pull/996) to enable the annotation of inferred axioms during release.

## Makefile workflows

- Make it possible to collect per-command resource usage data [PR](https://github.com/INCATools/ontology-development-kit/pull/940). This allows us to see which goals consume how much memory, and how long they take, to identify performance bottlenecks.
- Enable support for custom ROBOT plugins in ODK [PR](https://github.com/INCATools/ontology-development-kit/pull/968)
- Add a `test_fast` goal to allow running tests without refreshing dependencies [PR](https://github.com/INCATools/ontology-development-kit/pull/803)
- Re-integrate LightRDF RDF/XML validation [PR1](https://github.com/INCATools/ontology-development-kit/pull/850), [PR2](https://github.com/INCATools/ontology-development-kit/pull/928)
- Add SPARQL Check to find uses of deprecated DC [PR](https://github.com/INCATools/ontology-development-kit/pull/817)
- Add release diff action [PR](https://github.com/INCATools/ontology-development-kit/pull/737). This allows posting diffs automatically as a comment to a Pull Request.
- Add convenience check if customised ROBOT report config is out of date [PR](https://github.com/INCATools/ontology-development-kit/pull/998). This allows checking if you are missing out on some new ROBOT report checks!
- Add a nicer, more comprehensive way to understand the versions of the tools used in ODK [PR](https://github.com/INCATools/ontology-development-kit/pull/1011)

## Runner and Infrastructure

- Allow passing configuration options to the OWL API. [PR](https://github.com/INCATools/ontology-development-kit/pull/807)
- Automatically check whether the repository needs to be updated [PR](https://github.com/INCATools/ontology-development-kit/pull/873)
- Forward the host SSH agent socket into the container [PR](https://github.com/INCATools/ontology-development-kit/pull/853)

## Bugfixes

- Fix import to use OBOBASE in base-iri, not URIBASE [PR](https://github.com/INCATools/ontology-development-kit/pull/823)
- Do not create individual import modules when use_base_merging is enabled [PR](https://github.com/INCATools/ontology-development-kit/pull/829)
- Make docs workflow configurable [PR](https://github.com/INCATools/ontology-development-kit/pull/889)
- Update `illegal-date-violation.sparql` to accept `xsd:dateTime` [PR](https://github.com/INCATools/ontology-development-kit/pull/932)
- Update URL to show CI status badge correctly on repo README.md [PR](https://github.com/INCATools/ontology-development-kit/pull/978)

# v1.4

A full record of all changes can be seen [here](https://github.com/INCATools/ontology-development-kit/milestone/6?closed=1).

## New and updated tooling

- New [ROBOT Version 1.9.3](https://github.com/ontodev/robot/releases/tag/v1.9.3)
- A lot of [updated python tools](https://github.com/INCATools/ontology-development-kit/blob/master/constraints.txt), including [OAK (0.1.71)](https://github.com/INCATools/ontology-access-kit), [SSSOM tools](https://github.com/mapping-commons/sssom-py) (0.3.22), [LinkML](https://linkml.io/) (1.4.4) and [curies](https://github.com/cthoyt/curies) (0.4.2).
- `gh` is now installed in ODK, which means that GitHub workflows can be run directly through ODK. For example, try out the new `public_release` workflow which automatically creates a GitHub release for you.
- A full list of all available python tools and there vesions is available [here](https://github.com/INCATools/ontology-development-kit/blob/master/constraints.txt)

## New configuration options 

- Making the `uribase` configurable. You can now set the URI base in your `myont-odk.yaml` file to something different from http://purl.obolibrary.org/obo/, which enables developers from outside OBO to use ODK. Note that there is no guarantee that you can export your ontology to the OBO file format of you customise your `baseuri` this way!
- `import_component_format`: You can now configure the format in which your imports and components are serialised. For example, rather than owl (RDFXML), which used to be the default, you can set this option to ofn. For a complete reference see https://robot.obolibrary.org/convert.
- `mirror_type`: You can define the type of the mirror for each import. Supported: base, custom, no_mirror.
- `release_use_reasoner`: If false, no reasoning is performed for generating release files. This is only relevant for building application ontologies, where all components are already fully classified.
- `sparql_test_on`: You can define the list of input files to run the custom SPARQL queries. Supported: edit, and any release artefact, e.g myont-base.owl ([example](https://github.com/INCATools/ontology-development-kit/blob/master/tests/test-sparql-report.yaml)).
- `use_edit_file_imports`: If TRUE, use whatever imports you have in the edit file to create the release (default). If FALSE,  components (and imports) are merged into the release independent of whether they are mentioned in the edit file or not. This can help for example in cases where import modules are so large, they cannot be checked into version control.
- The `ci` option now takes `gitlab-ci` as a value, which sets your repo up with basic Continuous Integration Testing for GitLab.

## Makefile workflows

- Adding new `make reason_test` command ([pull](https://github.com/INCATools/ontology-development-kit/pull/639), [issue](https://github.com/INCATools/ontology-development-kit/issues/645))
- Adding intermediate artefact `$(TMPDIR)/$(ONT)-preprocess.owl` to the release workflow which enable the centralisation of preprocessing in a single make step. Basically, rather than creating release artefacts directly from the editors file (e.g. bfo-edit.owl), we add intermediate step from which all releases are derived. This intermediate can then be customised by the user ([pull](https://github.com/INCATools/ontology-development-kit/pull/639), [issue](https://github.com/INCATools/ontology-development-kit/issues/544))
- Introduces an experimental new release called "base-plus", which includes the inferred and non-redundant classification of the ontology. This is highly experimental and may be removed in a future release of ODK. The new goal is much more rigorous in removing axioms from other ontologies as well. The old base file can now be exported as an  "editors release" instead ([pull](https://github.com/INCATools/ontology-development-kit/pull/643), [issue](https://github.com/INCATools/ontology-development-kit/issues/646)).
- Introduces the option of skipping the use of reasoner during the release process (important for application ontologies), ([pull](https://github.com/INCATools/ontology-development-kit/pull/643), [issue](https://github.com/INCATools/ontology-development-kit/issues/644))
- Introduces a new mode that enable the use of ODK entirely without owl:imports in the edit file (this is great in case we want to use the ODK workflows but not check in any files, imports or components, into version control, like huge application ontologies), ([pull](https://github.com/INCATools/ontology-development-kit/pull/643), [issue](https://github.com/INCATools/ontology-development-kit/issues/629)).
- Adds a feature to directly support ROBOT templates in components ([example](https://github.com/INCATools/ontology-development-kit/blob/master/tests/test-templates.yaml)). Templates need to be activates with the project-level `use_templates: TRUE` option, and can then be used to define components, like in the example.
- Adds an option to do a `public_release` on Github which creates a GitHub release, tags it, and uploads release artefacts.
- Adds a `release_diff` workflow which creates a simple markdown report between the latest release and the current one.
- Adds a feature to directly support SSSOM mapping files, both in components and as standalone ([example](https://github.com/INCATools/ontology-development-kit/blob/master/tests/test-sssom.yaml)). This allows to curate, for example, SSSOM mapping files in tables and them release them as part of the general release process. It also allows extracting mappings from inside the Ontology automatically using the SSSOM toolkit.
- Changes in the `src/ontology/run.sh` wrapper script:
  - [It is now possible](https://github.com/INCATools/ontology-development-kit/pull/640) to execute the Docker image through [Singularity](https://apptainer.org).
  - The `IMAGE` variable, which can used to specify an alternative ODK image, [has been renamed](https://github.com/INCATools/ontology-development-kit/pull/655) to `ODK_IMAGE`.
  - A new variable `ODK_TAG` has been introduced, allowing to specify an alternative tag (default is `latest`). A tag may also be specified directly as part of the `ODK_IMAGE` variable (as in `ODK_IMAGE=odkfull:v1.3.1`).
  - A new variable `ODK_BINDS` has been introduced, allowing to specify extra bindings between a directory on the host computer and a directory inside the Docker container.
  - Variables used by the `run.sh` script can now be set in a `src/ontology/run.sh.conf` file, which will be sourced by the wrapper script.
  - With the config file option `use_env_file_docker`, if true, you can pass your local environment to the docker container. It is _strongly advised_ to add `run.sh.env` to `.gitignore` before using this feature. Committing your environment to git may reveal passcodes and other private information!


# v1.3.1

- [Update to ROBOT 1.9.0](https://github.com/INCATools/ontology-development-kit/pull/621), see [ROBOT release notes](https://github.com/ontodev/robot/releases/tag/v1.9.0). One major change concerning ODK: the [OBOGraphs JSON serialiser](https://github.com/geneontology/obographs) has been updated significantly, which means obographs json files may look a bit different. Most important change: empty elements (xrefs) are no longer serialised.
- Added shortcut make commands for recreating components: `recreate-components` and `recreate-%` ([pull](https://github.com/INCATools/ontology-development-kit/pull/570)).
- Added new shortcut command for fast releases: `make prepare_release_fast`.
- New tools:
  - [Ontology Access Kit](https://github.com/INCATools/ontology-access-kit), a python library for interacting with ontologies, the the ODK ([pull](https://github.com/INCATools/ontology-development-kit/pull/586)).
  - [gh](https://github.com/cli/cli): GitHub CLI for running releases, createing pull requests and more
  - [j2cli](https://github.com/kolypto/j2cli): Jinja template client
  - [rdftab](https://github.com/ontodev/rdftab.rs): RDF Tables with Rust
  - [gizmos](https://github.com/ontodev/gizmos): Python utilities for ontology development
  - Other: obographviz, node.js, graphviz, npm
- The ontology diff GitHub action, a tool that allows you to create diffs for you ontology pull requests, is now automatically synced with your ODK setup ([pull](https://github.com/INCATools/ontology-development-kit/pull/564)).
- Added `workflows` option to ODK config. This allows users to choose which workflows (at the moment GitHub actions-based) should be automatically synchronised.
- Custom ROBOT SPARQL reports now consider the imports by default ([pull](https://github.com/INCATools/ontology-development-kit/pull/570))
- [Base IRIs can now be configured for ROBOT report, similar to what OBO Dashboard does](https://github.com/INCATools/ontology-development-kit/pull/609/files)
- Technical
   - Run internal `make` and $(MAKE) to ensure that parameters are propagated correctly ([issue](https://github.com/INCATools/ontology-development-kit/issues/554)).
   - Mirror goal is only run when mirrors have been downloaded ([pull](https://github.com/INCATools/ontology-development-kit/pull/570))
   - src/ontology/run.sh can now be configured with a ODK_JAVA_OPTS parameter at runtime, rather than just with a `robot_java_args` option in the projects ODK config file. This allows to more easily run releases across environments with different levels of memory. Example: `ODK_JAVA_OPTS=-Xmx4G ODK_DEBUG=yes ./run.sh make odkversion`
   - src/ontology/run.sh warns the user in certain cases to update their local ODK image.
   - Better [linebreaks in Makefile](https://github.com/INCATools/ontology-development-kit/pull/612) to make lines more.
- Documentation
   - [Added improved `CONTRIBUTING.md` to ODK repo template](https://github.com/INCATools/ontology-development-kit/pull/620)
   - [Removed history.md page from ODK documentation](https://github.com/INCATools/ontology-development-kit/pull/611)
   - [Some improved settings to default mkdocs documentation pages](https://github.com/INCATools/ontology-development-kit/issues/605), such as better search, edit buttons and more.
   - Some improved documentation on components ([pull](https://github.com/INCATools/ontology-development-kit/pull/577))
   - All ODK-related general docs now moved to https://oboacademy.github.io/obook.
   - DOSDP documentation pages are now only created when dosdp is configured.
- Bugs
   - The automatic docs workflow now correctly `uses: mhausenblas/mkdocs-deploy-gh-pages@master`.
   - In ODK 1.3.0 `prepare_release` depended on `all`, which caused some cyclicity for some customised setups. This is now changed to a separate `all_odk` goal.
   - Simple ontology release artefacts now correctly depend on the `simple seed`.
   - Similar to subset declarations, ODK now injects synonymtype declarations when extracting a module.
   - diff.yaml no longer [added by default](https://github.com/INCATools/ontology-development-kit/issues/588), has to be configured.
   


# v1.3.0 (24 February 2022)

### New features:

- _New DOSDP workflow for matching patterns_: This is a powerful workflow that "matches" your DOSDP YAML templates against your ontology to actually _create_ TSVs - so the other way around of what we usually do.
  - To set this up, you introduce a new "pattern_pipelines_group" called `matches`, which can then be invoked with `sh run.sh make dosdp-matches-%` to match all configured DOSDP tempates with the ontology.
  - Example see [here](tests/test-dosdp-matches.yaml).
- _Experimental feature-diff feature_: When creating a pull request, the ODK can now automatically make a comment to the pull request informing editors of changes to the ontology ([issue](https://github.com/INCATools/ontology-development-kit/pull/547))
- _Adding [Relation Graph](https://github.com/balhoff/relation-graph/) to ODK_ ([pull request](https://github.com/INCATools/ontology-development-kit/pull/535), [pull request](https://github.com/INCATools/ontology-development-kit/pull/529))
- _New QC checks_: 
  - _IRIs in labels_: Often when using autogenerated labels in DOSDP we do not realise we are accidentally missing labels to for generating class names. We introduced a QC check to protect against that ([pull request](https://github.com/INCATools/ontology-development-kit/pull/542/files), [issue](https://github.com/INCATools/ontology-development-kit/issues/536))
  - Ensuring that the range of  never_in_taxon:, present_in_taxon: , oboInOwl:inSubset, rdfs:seeAlso, foaf:depicted_by and dcterms:contributor is always IRI ([issue](https://github.com/INCATools/ontology-development-kit/issues/520), [pull request](https://github.com/INCATools/ontology-development-kit/pull/527/files))
- Switched the default Ontology documentation theme from `readthedocs` to `material` ([pull request](https://github.com/INCATools/ontology-development-kit/pull/530/files))
- New [DOSDP tools version 0.19.1](https://github.com/INCATools/dosdp-tools/releases/tag/v0.19.1)

### Bugfixes:
- Many faulty dependencies in the Makefile that triggered unnecessary re-runs of make were removed ([issue](https://github.com/INCATools/ontology-development-kit/issues/448))
- Some major refactoring of the main `Makefile` ([pull request](https://github.com/INCATools/ontology-development-kit/pull/530/files)). This includes, in particular, a smarter way to deal with web-dependencies (mirrors, dosdp-templates, components).
- Fixes to documentation ([Managing dependencies with base files](https://github.com/INCATools/ontology-development-kit/issues/514), [Import seed system](https://github.com/INCATools/ontology-development-kit/pull/519))
- Some fixes to DOSDP pipeline setup ([issue](https://github.com/INCATools/ontology-development-kit/issues/490))
- Git `main` branch was hardcoded to `master` during the seeding process, now uses the ODK config file ([pull request](https://github.com/INCATools/ontology-development-kit/pull/541), [issue](https://github.com/INCATools/ontology-development-kit/issues/508))
- Making sure the repo seeding process preserves file privileges. This ensures, in particular, that `run.sh` is executable and can be run using `./run.sh` instead of `sh run.sh` ([issue](https://github.com/INCATools/ontology-development-kit/issues/196), [pull](https://github.com/INCATools/ontology-development-kit/pull/538))
- DOSDP Validation now [uses python up to date library](https://github.com/INCATools/ontology-development-kit/pull/515)
- Auto-deployment of ODK docs fixed (ODK internal, [pull request](https://github.com/INCATools/ontology-development-kit/pull/517)), but much of ODK's docs has moved to [OBOOK (OBO Academy)](https://oboacademy.github.io/obook/)
- Fixing some issues with default values when using `robot_report` in your ODK config ([pull request](https://github.com/INCATools/ontology-development-kit/pull/558))

### New commands:
- `sh run.sh make help`: show frequently used ODK commands and their usage ([issue](https://github.com/INCATools/ontology-development-kit/issues/531))
- `sh run.sh make TSV=my.tsv validate-tsv`: Experimental TSV validation feature with [TSValid](https://github.com/INCATools/ontology-development-kit/issues/532) ([issue](https://github.com/INCATools/ontology-development-kit/issues/375))
- `sh run.sh make validate-all-tsv`: Validate all TSV tables configured in repo with [TSValid](https://github.com/ontodev/tsvalid) ([issue](https://github.com/INCATools/ontology-development-kit/issues/375))
- `sh run.sh make dosdp-matches-%`: Run the "matches" pipeline, see above. ([issue](https://github.com/INCATools/ontology-development-kit/issues/540))
- `sh run.sh make clean`: Clean up some temporary files created by the build. ([issue](https://github.com/INCATools/ontology-development-kit/issues/300))

### Recommendations for ontology maintainers:

- We have overhauled the SPARQL query management to make it more customisable ([pull request](https://github.com/INCATools/ontology-development-kit/pull/523)). We recommend, before updating to the latest ODK, to delete old and potentially stale SPARQL queries like this: `rm ../sparql/owldef-violation.sparql ../sparql/nolabels-violation.sparql ../sparql/def-lacks-xref-violation.sparql ../sparql/obsolete-violation.sparql ../sparql/redundant-subClassOf-violation.sparql`.
- You should periodically review the contents of your `src/ontology/custom.Makefile` - if you overwrite a lot of goals, you should review wether the overwrite is still necessary. This ODK release has a lot of revisions to the Makefile, so this should be a good opportunity to check this!

# v1.2.32 (16 December 2021)
- Updated to [ROBOT 1.8.3](https://github.com/ontodev/robot/releases/tag/v1.8.3), which removes Log4J and [fixes some issues](https://github.com/ontodev/robot/blob/master/CHANGELOG.md#183---2021-12-16)

# v1.2.31 (3 December 2021)
- Updated to [ROBOT 1.8.2](https://github.com/ontodev/robot/releases/tag/v1.8.2)
- Updated to [DOSDP tools 0.18](https://github.com/INCATools/dosdp-tools/releases/tag/v0.18)
- Adding `use_base_merging` to config files, which _enables the BASE file pipeline_, a completely different way to handle imports. This feature is not ready for primetime, but if you are interested in testing this, get in touch. For more details read ([pull](https://github.com/INCATools/ontology-development-kit/pull/496/files)).
- Adding back [ssh/scp](https://github.com/INCATools/ontology-development-kit/issues/494)
- Migrated to Java 11 as the base Java in ODK ([pull](https://github.com/INCATools/ontology-development-kit/pull/492))
- Adding `make_base` feature that allows to autogenerate base files from ontologies where they do not exist ([pull](https://github.com/INCATools/ontology-development-kit/pull/496/files))
- Adding new command `sh run.sh make no-mirror-refresh-imports` which refreshes imports without refreshing mirrors. Can be used for individual ontologies as well.
- Making `owltools` where necessary configurable with a bespoke memory parameter ([pull](https://github.com/INCATools/ontology-development-kit/pull/487))
- Fixing the GitHub action to auto-deploy the documentation ([pr](https://github.com/INCATools/ontology-development-kit/pull/485)).
- Fixed a bug where the [DOSDP pages in ODK where generated in the wrong part](https://github.com/INCATools/ontology-development-kit/pull/496/files) of the mkdocs documentation.
- New command `sh run.sh make explain_unsat` which generates a nicely formatted set of explanations for your unsatisfiable classes ([pull](https://github.com/INCATools/ontology-development-kit/pull/493/files))
- Adding method to [measure the memory consumption of your builds](https://github.com/INCATools/ontology-development-kit/pull/495). For example, you can now run `IMAGE=odklite ODK_DEBUG=yes ./run.sh make prepare_release` to run your release on the (much lighter) `odklite` container of ODK, and get a nice benchmark summary at the end: 
```
### DEBUG STATS ###
Elapsed time: 7:49.24
Peak memory: 6517356 kb
```
- _Breaking changes_:
  - OBO Modules are no longer generated automatically. You can use the `export_obo` option to add them back  ([pull](https://github.com/INCATools/ontology-development-kit/pull/496/files))
  - Equivalent class default setting changed from `all` to `asserted only` ([pull](https://github.com/INCATools/ontology-development-kit/pull/497)). This means that from now on, if you dont change the setting deliberately, your pipeline will fail if their are equivalent classes that are not deliberately asserted.
  - OWL 2 DL profile checking is now `true` by [default](https://github.com/INCATools/ontology-development-kit/pull/481). You have to actively switch it off by setting `ensure_owl2dl_profile` to `FALSE` in your config file. 

# v1.2.30 (11 October 2021)
- Important: The way we install python packages has changed significantly: we are now using _fixed version dependencies_ ([issue](https://github.com/INCATools/ontology-development-kit/issues/463)). If there are problems with the versions of packages we are using, please let us know immediately.
- We are now using multi-stage builds in ODK for docker. The `obolibrary/odklite` container is considerably lighter (smaller) than the normal `odkfull` container you have been using so far, and it should be sufficient for most ODK pipelines.
- Mirrors are now downloaded with CURL instead of ROBOT, and configurable with `mirror_retry_download` and `mirror_max_time_download` in the `import_group` section of the ODK config file ([PR](https://github.com/INCATools/ontology-development-kit/pull/474)). *Note that the default `mirror_max_time_download` is 200 sec (a bit more than 3 minutes), which may be tight for some huge ontologies*.
- odkfull now includes Soufflé.
- For those who are using DOSDP patterns we re-introduced the pattern schema check even if pattern generation is skipped (it is very fast).
- Created a simple way to cite ODK from within GitHub, using the CITATION.cff file. If you go to https://github.com/INCATools/ontology-development-kit, you will now see a "cite this repo" section under the *About* section.
- Changed the default README.md to include a better reference to ODK, the correct ontology description text and the correct edit file extension.
- Added a GitHub action to deploy the ODK-based mkdocs documentation ([issue](https://github.com/INCATools/ontology-development-kit/issues/478)).
- Created a [page](https://github.com/INCATools/ontology-development-kit/blob/master/docs/FrequentlyUsedODKCommands.md) for frequently used ODK commands.
- Bugfixes:
  - project repo name was not read correctly during `make update_repo` causing it to be named "False" ([commit](https://github.com/INCATools/ontology-development-kit/commit/856a7f63c6b24b614eeae07deaf8ef1724903473))
  - Fixed a bug where mirrors were not considered precious
  - Fixed a bug where where the report directories where not created when running a sparql report command ([commit](https://github.com/INCATools/ontology-development-kit/commit/dc1bb2220b978ed9adfb7cf9d2924ea6224945e3))
  - Fixed a bug where `report` command incorrectly did not include components in the check ([issue](https://github.com/INCATools/ontology-development-kit/issues/447))
  - Fixed a bug where myont-odk.yaml was not created when using command line mode during seeding ([issue](https://github.com/INCATools/ontology-development-kit/issues/384))
  - Added some tests for external tools ([issue](https://github.com/INCATools/ontology-development-kit/issues/472)) to ODK built process
  - Konclude now works on the arm64 variant.




# v1.2.29 (11 June 2021)
- Switched to a more up-to-date base image (ubuntu-20.04, [pull](https://github.com/INCATools/ontology-development-kit/pull/434))
- Lots of technical changes on how to manage releases on dockerhub, especially multi-arch (same image should now work on M1, i.e. arm64 and amd64 machines, [pull](https://github.com/INCATools/ontology-development-kit/pull/429))
- Pip install operations now using `python3 -m pip` ([pull](https://github.com/INCATools/ontology-development-kit/pull/439))
- Introduced a new option (`remove_owl_nothing`) in repo config to remove mentions of owl:Nothing in releases
- New python packages: linkml, kgx and funowl
- Moved a comprehensive test suite to GitHub actions ([pull](https://github.com/INCATools/ontology-development-kit/pull/427))
- Updated the [documentation](https://github.com/INCATools/ontology-development-kit/blob/master/docs/CreatingRepo.md) on how to create a new repo with the ODK
- Updated Repo [README](https://github.com/INCATools/ontology-development-kit) with more docs, a list of significant external contributors (please just let me know if anyone else needs to be added), core team etc.
- Bugfixes: 
   - Unnecessary use of `.FORCE` in custom components removed ([pull](https://github.com/INCATools/ontology-development-kit/pull/432))
   - Fix another bug with OWL DL profile validation ([pull](https://github.com/INCATools/ontology-development-kit/pull/430))
   - Changed the `-g/--skipgit` option be be a flag ([pull](https://github.com/INCATools/ontology-development-kit/pull/428))
   - Some fixes to how subsets are handled ([pull](https://github.com/INCATools/ontology-development-kit/pull/424/files?file-filters%5B%5D=.jinja2))


# v1.2.28 (6 May 2021)
- New DOSDP tools version [0.17](https://github.com/INCATools/dosdp-tools/releases/tag/v0.17)
- Major: made the new image compatible with M1! Thanks to @gouttegd who did all the hard work. Super excited about this!
- Some major fixes to the automatic documentation generator, see for example https://pato-ontology.github.io/pato/. Please get in touch if you want help setting up your own awesome documentation site!
- A bug fix in the OWL2DL validation pipeline for testing
- A bug fix for the subset injection during Module creation, see [here](https://github.com/INCATools/ontology-development-kit/issues/411)
- Minor fixes to GitHub instructions (switching wordings from master to main)

# v1.2.27 (4 April 2021)
- revived odklite image with a minimum install (smaller in size than odkfull, with just robot and owltools!)
- revived robot image with just robot installed
- Added Jena 3.12.0 to odkfull image
- Added module configs (see docs)
- added a complete new documentation system for ontologies using mkdocs (see docs)
- added OWL2 DL profile checking (see [here](tests/test-robot-validate-profile.yaml) for example)
- Added sqlite3, dos2unix, and aha to odkfull image
- Added a `use_custom_import_module` feature (see docs for example)
- Added ability to add completely customised release artefacts (see Uberon repo for example)
- Revised update mechanism. Please run the `make update_repo` *multiple times if you encounter problems and to ensure that all changes are picked up*.

# v1.2.26 (10 February 2021): HOTFIXES
- Hotfixes:
  - The new mireot module technique was buggy and is therefore removed again. Sorry; we will try again next time. You can still use the `custom` option to implement mireot yourself!
  - A change in the way imports were processed introduced a very high memory footprint for large ontologies and slowed stuff down. If you do not have a lot of memory (and time!) available, you should use the following new flags: `is_large` and `use_gzipped`. `is_large: TRUE` introduces a special handling for the ontology that is faster and consumes less memory when creating an import. Using `use_gzipped` will try to download the ontology from its gzipped location. Make sure its actually there (we know its the case for chebi and pr at least)!
```
import_group:
  products: 
    - id: pr
      use_gzipped: TRUE
      is_large: TRUE
    - id: chebi
      use_gzipped: TRUE
      is_large: TRUE
```
  - An irrelevant file (keeprelations.txt) was still generated even if needed when seeding a new repo.
  - Module type `STAR` was accidentally hard coded default for slme. Now changed to `BOT` as it was.
  - CI configs where not correctly copied by update routine. Now it does. Note for the changes to be picked up, you need to run `sh run.sh make update_repo` twice (once for updating the update script itself)!
  - Geeky (but necessary) all phony make goals are now correctly declared as `.PHONY`.
- Some last minute features:
  - In new repos, the README.md is now generated with the correct, appropriate banners.
  - We now have a new feature, `custom_makefile_header`, that allows injecting a custom header into the Makefile. Most mortals wont need this, but this is how it goes:
```
custom_makefile_header: |
  ### Workflow
  #
  # Tasks to edit and release OMRSE.
  #
  # #### Edit
  #
  # 1. [Prepare release](prepare_release)
  # 2. [Refresh imports](all_imports)
  # 3. [Update repo to latest ODK](update_repo)
```
- all features and fixes here: https://github.com/INCATools/ontology-development-kit/pull/397

# v1.2.26 (2 February 2021)
- New versions:
  - fastobo validator to new version ([pull](https://github.com/INCATools/ontology-development-kit/pull/379)
  - ROBOT 1.8.1 (lots of new changes, see: [Changelog](https://github.com/ontodev/robot/blob/master/CHANGELOG.md))
  - DOSDPTOOLS 0.16 (lots of speed-up for bulk pattern generation)
- New features:
  - new python dependencies ([cogs](https://github.com/ontodev/cogs), a tool to directly manage tsv files in your repo on Google sheets)
  - stable serialisation order for JSON files using jq's walk function. -> this decreases the size of the diff for git!
  - Some improvements to logging when seeding a new repo, to make it easier to find errors
  - A new method to validate the id-ranges file can be invoked using `sh run.sh make validate_idranges` (after update to latest ODK repo)
  - modules are now annotated with a dc:source annotation to their original ontology (version)
- New configuration options:
  - module_type ([example slme](tests/test-module-star.yaml), [example minimal](tests/test-module-minimal.yaml), [example mireot](tests/test-module-star.yaml)). Direct support for MIREOT and a new module type, minimal.
  - To encourage stable versions and releases, ODK, by default, merges imports into the release files. Previously, we continued to release the imports as well - which we do not recommend anymore. If you still wish to release your imports as usual, you can set a flag `release_imports` in the `import_group` section of your makefile (see [example](tests/test-release.yaml)).
  - the same as the above applies for reports (see [example](tests/test-robot-report.yaml))
  - The custom sparql checks, and the custom sparql exports, are now directly configurable
    - `custom_sparql_checks` : Chose which additional sparql checks you want to run. The related sparql query must be named CHECKNAME-violation.sparql, and be placed in the src/sparql directory (see [example](tests/test-robot-report.yaml))
    - `custom_sparql_exports` : Chose which additional sparql checks you want to run. The related sparql query must be named CHECKNAME-violation.sparql, and be placed in the src/sparql directory (see [example](tests/test-robot-report.yaml))
    - `custom_sparql_exports` : Chose which custom reports to generate. The related sparql query must be named CHECKNAME.sparql, and be placed in the src/sparql directory (see [example](tests/test-robot-report.yaml))
  - `git_main_branch` : The `main` branch for your repo, default `main`, or (now discouraged, previously) `master`.
  - `ci`: continuous integration defaults; currently available: `travis`, `github_actions`
  - `create_obo_metadata`: This is mainly for new OBO ontologies. If true, OBO Markdown and PURL configs are created.
  - `export_project_yaml`: Default `False`. If set to `True`, project.yaml is created in the top level of the repo.
- Removed a few files from the standard config. This is all part of an effort to slimming down the ODK to the least number of necessary files checked into version control: `src/ontology/Dockerfile`,`src/ontology/patterns.sh`, `src/ontology/release.sh`, `src/ontology/test.sh`, and some temporary files. The `patterns` directory and all its contents only appear now when `use_dosdps`=TRUE.
- Technical:
  - Refactored ODK Dockerfile (merged some layers)
  - added jq 1.6 which is not available via apt-get (yet).
  - added sssom python package, but its in so alpha-alpha state, it should be used with caution

# v1.2.25 (18 November 2020)
- Updated ROBOT to new version 1.7.2, which includes some hotfixes for ROBOT report and update to whelk 1.0.4
- Fixed a bug (https://github.com/INCATools/ontology-development-kit/issues/376) that prevented certain things (like imports and pattern generation processes) to be printed when running the Makefile.

# v1.2.24 (6 November 2020)
- Updated ROBOT to new version 1.7.1
- Added the (highly experimental) ability to ODK to run OBO dashboard (see [instructions and examples](https://github.com/INCATools/ontology-development-kit#running-obo-dashboard-with-odk)).
- Added more python packages to ODK, see [requirements.txt](requirements.txt.full).
- Added a new set of configurations for ROBOT report. WARNING:
`report_fail_on` option is now deprecated in favour of a new block of options:

```
robot_report:
  use_labels: TRUE
  fail_on: None
  custom_profile: TRUE
  report_on:
    - .owl
    - .obo
    - edit
```

- `use_labels`: allows switching labels on and off in the ROBOT report, see [here](http://robot.obolibrary.org/report#labels)
- `fail_on`: is the old `report_fail_on` option, see [here](http://robot.obolibrary.org/report#failing).
- `custom_profile`: allows switching on custom profiles, see [here](http://robot.obolibrary.org/report#profiles)
- `report_on` allows specifying which files to run the report over (for example hp.owl, hp.obo, hp-edit.owl).

# updated v1.2.23 (6 August 2020)
- Added new version of fastobo (v0.3.0)
- Added rdflib to Python environment
- Added xlsx2csv command line tool

# v1.2.23 (6 August 2020)
- New ROBOT (v 1.7.0)
- New owltools (v. 2020-04-06)
- Added [SWI Prolog](https://www.swi-prolog.org/) and C. Mungall's [sparqlprog](https://github.com/cmungall/sparqlprog) tools
- Release artefacts are now annotated with `owl:versionInfo`
- run.sh now got the `JAVA_OPTS` parameter which is necessary to set the maximum memory allowed for owltools 
- Bugs:
  - base-modules are now correctly annotated with resource references rather than strings ([issue](https://github.com/INCATools/ontology-development-kit/pull/333))
  - The ODK_VERSION variable in the Makefile was misnamed, which causes a circularity with updating it correctly when the Makefile is updated with a new ODK. This is fixed, but for the fix to kick in, you have to run `sh run.sh make update_repo` twice this time!
  
# v1.2.22 (23 February 2020)
- New ROBOT (v. 1.6.0)
- Bugfixes: 
  - Small fixes to [update_repo method](https://github.com/INCATools/ontology-development-kit/issues/305)
  - the sparql query for [extracting labeled subsets](https://github.com/INCATools/ontology-development-kit/issues/146) is now fixed
  - Some unneeded files (ontologyterms.txt) are removed from the default template.
  - a few more files are added to the [.gitignore file](https://github.com/INCATools/ontology-development-kit/issues/317)
  - The [catalog file is restructured](https://github.com/INCATools/ontology-development-kit/issues/105) to preclude Protege from changing it in unwanted ways.
  - the license in the ontology metadata is now required to be an IRI rather than a string.
  - The odk.py should now be executable in a [non-docker context](https://github.com/INCATools/ontology-development-kit/issues/312)
  - JSON versions of imports are not anymore generated. OBO versions are only generated if OBO is used as the edit file serialisation.
  - PAT=false now skips pattern download
- Fixes to DOSDP pipeline
  - DOSDP tools is updated to version 0.14. This version comes with some great changes, including:
    - a mode in which multiple patterns can be compiled at once (batch mode)
    - we finally have have optional columns and column values!
  - external.txt can now be empty
  - instead of abnormalAnatomicalEntity, an example.yaml is added to the default pattern directory
- Infrastructure (only relevant to ODK developers):
  - The test framework for ODK is now more dynamic: 
    1. Travis now correctly builds the ODK from scratch and runs the tests against the new build version
    1. Instead of adding new tests to the Makefile, you can simply now drop a new YAML file into the tests/ directory.
  - ODK Dockerfile has been optimised a bit for size (avoiding superfluous chmod calls)
  - the yaml loader in the ODK is now replaced by a safe loader

# v1.2.21 (23 January 2020)
- switched the Docker base image to ubuntu:18.04
- Added ammonite to the container

# v1.2.20 (2 January 2020)
- updated ROBOT to version 1.5.0
- base modules now get a special "base module" ontology annotation
- some bug fixes of the makefile process:
  - pattern file download
  - simple seed now takes into account annotation properties 
  - subset annotation handling improved

# v1.2.19 (21 October 2019)
- added functionality to update the repository after changing the yaml config. **This feature is still experimental.** To make use of this, you need to update your Makefile and copy the file under src/scripts/update_repo.sh in the respective folder of your repository. You should then be able  to run `sh run.sh make update_repo` to get your whole repo to the latest state. Be careful though: some files like the Makefile, run.sh and the sparql queries are considered native to ODK; this update routine will overwrite those files. Therefore, check your git diff before committing anything you might not want. 
- similar to `sh run.sh make IMP=false prepare_release`, it is now possible to skip pattern generation when creating a release `sh run.sh make PAT=false prepare_release`
- Bug fix to component pipeline
- Bug fix to report print out
- You can now exclude tautologies from your releases, such as Nothing SubClassOf Nothing or similar. For more information about this brand new ROBOT feature see http://robot.obolibrary.org/reason#excluding-tautologies. You can change the default behaviour by adding `exclude_tautologies: false` or `exclude_tautologies: all` to your yaml config.
- Bug fix to how external.txt is handled (pattern pipeline)

# v1.2.18 (13 September 2019)
- Upgrade ROBOT to version 1.4.3
- Minor bug fix in handling temporary file directories

# v1.2.17 (10 September 2019)
- Bug fix Konclude reasoner invocation
- Bug fix simple seed generation
- Bug fix: main owl release file (ont.owl) now has the correct version IRI
- More debugging output during seeding process
- Updated some of the documentation to be more generic towards GitHub vs GitLab and others 
- Highly experimental features (not for production) that allows the use of GitHub api for making a GitHub [release programmatically](https://github.com/INCATools/ontology-development-kit/pull/268/files). For an example config see [here](https://github.com/INCATools/ontology-development-kit/blob/master/examples/tests/test-github-release.yaml). This feature is likely to change significantly over time. 
- The ODK version is now written into the Makefile, and is printed by default during runs of the ODK
- Bug fix that caused OBO file releases to have broken subset declarations (injection of subset annotation property by default in imports).
- It is now possible to tag releases with the date of release. Use: `release_date: True` in the configuration file 


# v1.2.16
*Major revisions of Makefile*

- *NOTE: for some of the new goals, a tmp directory is required in src/ontology directory (src/ontology/tmp)*
- Use ont.Makefile file to extend your default ODK make pipeline (which continues to be in src/ontology/Makefile). See [here](https://github.com/obophenotype/human-phenotype-ontology/blob/master/src/ontology/hp.Makefile) for an example;
- Use `allow_equivalents: assert-only` or `allow_equivalents: none` in your project configuration file ([Example](https://github.com/INCATools/ontology-development-kit/blob/master/examples/phenotype-ontologies/mp-odk.yaml)).
- Integrate components in your projects. A component is a part of your ontology that is managed somewhere outside of the edit file, for [example](https://github.com/INCATools/ontology-development-kit/blob/master/examples/phenotype-ontologies/wbphenotype-odk.yaml) and external file with logical definitions, or a set of xrefs imported from an external file.
  ```
  components:
    products:
      - filename: wbphenotype-equivalent-axioms-subq.owl
  ```
- you can now supply a different catalog.xml then the default by adding a line to your config file: `catalog_file: catalog-v001.xml`
- You can now run the [Konclude](http://derivo.de/en/products/konclude/) reasoner. See [here](https://github.com/FlyBase/drosophila-phenotype-ontology/blob/master/src/ontology/dpo.Makefile) for an integrated example.
- new release artefacts, which are documented [here](https://github.com/INCATools/ontology-development-kit/blob/master/docs/ReleaseArtefacts.md). Note that the simple and basic releases are currently highly experimental; we are working on maturing them.
- it is now possible to skip git related operations during the seeding process: `./seed-via-docker.sh -c --skipgit True -C odkconfig.yaml`. This is useful if the goal is to quickly regenerate the Makefile for example in the context of upgrading a repository.
- it is now possible to set [dates from the outside of the docker](https://github.com/INCATools/ontology-development-kit/issues/232) container as a parameter.
- it is now possible to run a OBO validor (see [here](https://github.com/INCATools/ontology-development-kit/pull/215))

# v1.2

**MAJOR OVERHAUL OF FRAMEWORK**

This release sees the introduction of project.yaml files (see
[examples/](examples)). Although command line passing of parameters is
still supported, the use of a project file is strongly encouraged.

Previously the following commands may be have been passed: `-c -d pato -d cl -d ro -t my-ontology myont`

Now you can use a yaml file:

```
id: myont
title: my ontology
import_group:
  products:
   - id: ro
   - id: cl
   - id: pato
```

## Changes for Users

 * project.yaml files can be passed instead of command line settings
 * Docker container can now be executed anywhere, no checkout required
 * Added [README-developers.md](CONTRIBUTING.md) for ODK developers
 * Docker container tracking ROBOT v1.2
 * Previously multiple dependencies: `-d ont1 ont2 ... ontN`, now `-d ont1 -id ont2 ... -d ontN`
 * New command line option `--source` to pass in an existing ontolgy-edit file

## Changes for ODK Developers

 * Dockerfile for odkfull now at root directory
 * Dockerfile now based on alpine
 * Perl script gone; new python script (Python3.6 required)
 * Uses Jinja2 templating system, including dynamic file templating

## Migration Guide

This will be complex BUT the new system will make future development easier.

You MAY want to wait for future incremental releases which will
include migration tools. But if you want to forge ahead, we recommend
creating a new repo and copying files across manually.

# v1.1.3

## Changes

 * fixing bug in which running seed-via-docker did not enter interactive mode when no arguments provided
 * added convenience wrapper scripts

## Migration guide

 * New .sh scripts in src/ontology can be directly copied across

# v1.1.2

## Changes

 * added interactive mode
 * added [DOSDP](https://github.com/INCATools/dead_simple_owl_design_patterns/blob/master/src/simple_pattern_tester.py) support

## Docker

 * [odkfull](https://hub.docker.com/r/obolibrary/odkfull/tags/) v1.1.2 includes robot 1.1.0

## Migration guide

This release adds a new template in the `src/patterns` folder. These can be copied across to an existing repo.

# v1.1.1

## Changes

Name of repo has changed to ontology-developer-kit

 * changing name of docker image to odk
 * Upgrade dosdp-tools to release 0.9.
 * Make docker commands workable on windows
 * Dockerize travis
 * Imports automatically generated
 * Added python dosdp checker to docker, fixes #55
 * use robot not owltools in all places

## Docker

odklite and odkfull 1.1.1 released. Note that new versions may be released independent of odk

 * robot pre-1.1.0
 * dosdp-tools 0.9

The docker release includes a pre-release of [robot 1.1.0](https://github.com/ontodev/robot/releases/tag/v1.1.0).
This is identical to 1.1.0, except for https://github.com/ontodev/robot/commit/928503b1303c139fc1cf4fc1939d64bda0f2ae30

## Migration guide

If you built your repo from a previous version of ODK, here is a rough guide to migrating:

 * Update your .travis.yml, in order to use Docker (optional but recommended)
 * change the name of the docker image to odkfull in your run.sh

# 1.1.0

 * Add a run.sh in the template for Docker
