
## ODK Project Configuration Schema

- **`allow_equivalents`** *(string)*: can be all, none or asserted-only (see ROBOT documentation: http://robot.obolibrary.org/reason). Default: `"asserted-only"`.


- **`catalog_file`** *(string)*: Name of the catalog file to be used by the build. Default: `"catalog-v001.xml"`.


- **`ci`** *(list)*: continuous integration defaults; currently available: travis, github_actions, gitlab-ci. Default: `["github_actions"]`.
  - **Items** *(string)*


- **`components`**: Refer to *[#/definitions/ComponentGroup](#definitions/ComponentGroup)*. Block that includes information on all ontology components to be generated.


- **`contact`** *(string)* Single contact for ontology as required by OBO.


- **`contributors`** *(list)* List of ontology contributors (currently setting this has no effect).
  - **Items** *(string)*


- **`create_obo_metadata`** *(boolean)*: if true OBO Markdown and PURL configs are created. Default: `true`.


- **`creators`** *(list)* List of ontology creators (currently setting this has no effect).
  - **Items** *(string)*


- **`custom_makefile_header`** *(string)*: A multiline string that is added to the Makefile. Default: `"\n# ----------------------------------------\n# More information: https://github.com/INCATools/ontology-development-kit/\n"`.


- **`description`** *(string)*: Provide a short description of the ontology. Default: `"None"`.


- **`documentation`**: Refer to *[#/definitions/DocumentationGroup](#definitions/DocumentationGroup)*. Block that includes information on all ontology components to be generated.


- **`dosdp_tools_options`** *(string)*: default parameters for dosdp-tools. Default: `"--obo-prefixes=true"`.


- **`edit_format`** *(string)*: Format in which the edit file is managed, either obo or owl. Default: `"owl"`.


- **`ensure_valid_rdfxml`** *(boolean)*: When enabled, ensure that any RDF/XML product file is valid. Default: `true`.


- **`exclude_tautologies`** *(string)*: Remove tautologies such as A SubClassOf: owl:Thing or owl:Nothing SubclassOf: A. For more information see http://robot.obolibrary.org/reason#excluding-tautologies. Default: `"structural"`.


- **`export_formats`** *(list)*: A list of export formats you wish your release artefacts to be exported to, such as owl, obo, gz, ttl. Default: `["owl", "obo"]`.
  - **Items** *(string)*


- **`export_project_yaml`** *(boolean)*: Flag to set if you want a full project.yaml to be exported, including all the default options. Default: `false`.


- **`extra_rdfxml_checks`** *(boolean)*: When enabled, RDF/XML product files are checked against additional parsers. Default: `false`.


- **`git_main_branch`** *(string)*: The main branch for your repo, such as main, or (now discouraged) master. Default: `"main"`.


- **`git_user`** *(string)*: GIT user name (necessary for generating releases). Default: `""`.


- **`github_org`** *(string)*: Name of github org or username where repo will live. Examples: obophenotype, cmungall. Default: `""`.


- **`gzip_main`** *(boolean)*: if true add a gzipped version of the main artefact. Default: `false`.


- **`id`** *(string)*: OBO id for this ontology. Must be lowecase Examples: uberon, go, cl, envo, chebi. Default: `""`.


- **`import_component_format`** *(string)*: The default serialisation for all components and imports. Default: `"ofn"`.


- **`import_group`**: Refer to *[#/definitions/ImportGroup](#definitions/ImportGroup)*. Block that includes information on all ontology imports to be generated.


- **`import_pattern_ontology`** *(boolean)*: if true import pattern.owl. Default: `false`.


- **`license`** *(string)*: Which license is ontology supplied under - must be an IRI. Default: `"https://creativecommons.org/licenses/unspecified"`.


- **`namespaces`** *(list)* A list of namespaces that are considered at home in this ontology. Used for certain filter commands.
  - **Items** *(string)*


- **`obo_format_options`** *(string)*: Additional args to pass to robot when saving to obo. TODO consider changing to a boolean for checks. Default: `""`.


- **`owltools_memory`** *(string)*: OWLTools memory, for example 4GB. Default: `""`.


- **`pattern_pipelines_group`**: Refer to *[#/definitions/PatternPipelineGroup](#definitions/PatternPipelineGroup)*. Block that includes information on all DOSDP templates used.


- **`primary_release`** *(string)*: Which release file should be published as the primary release artefact, i.e. foo.owl. Default: `"full"`.


- **`public_release`** *(string)*: if true add functions to run automated releases (experimental). Current options are: github_curl, github_python. Default: `"none"`.


- **`public_release_assets`** *(list)* A list of files that gets added to a github/gitlab/etc release (as assets). If this option is not set (None), the standard ODK assets will be deployed.
  - **Items** *(string)*


- **`reasoner`** *(string)*: Name of reasoner to use in ontology pipeline, see robot reason docs for allowed values. Default: `"ELK"`.


- **`release_artefacts`** *(list)*: A list of release artefacts you wish to be exported. Supported: base, full, baselite, simple, non-classified, 
    simple-non-classified, basic. Default: `["full", "base"]`.
  - **Items** *(string)*


- **`release_date`** *(boolean)*: if true, releases will be tagged with a release date (oboInOwl:date). Default: `false`.


- **`release_diff`** *(boolean)*: When enabled, a diff is generated between the current release and the new one. Default: `false`.


- **`release_materialize_object_properties`** *(list)* Define which object properties to materialise at release time.
  - **Items** *(string)*


- **`release_use_reasoner`** *(boolean)*: If set to True, the reasoner will be used during the release process. The reasoner is used for three operations:
    reason (the classification/subclassOf hierarchy computaton); materialize (the materialisation of simple existential/
    object property restrictions); reduce (the removal of redundant subclassOf axioms). Default: `true`.


- **`remove_owl_nothing`** *(boolean)*: Flag to set if you want odk to remove owl:Nothing from releases. Default: `false`.


- **`repo`** *(string)*: Name of repo (do not include org). E.g. cell-ontology. Default: `""`.


- **`robot_java_args`** *(string)*: Java args to pass to ROBOT at runtime, such as -Xmx6G. Default: `""`.


- **`robot_report`** *(object)*: Block that includes settings for ROBOT report, ROBOT verify and additional reports that are generated. Default: `{"custom_profile": false, "custom_sparql_checks": ["owldef-self-reference", "iri-range", "label-with-iri", "multiple-replaced_by", "dc-properties"], "custom_sparql_exports": ["basic-report", "class-count-by-prefix", "edges", "xrefs", "obsoletes", "synonyms"], "ensure_owl2dl_profile": true, "fail_on": null, "release_reports": false, "report_on": ["edit"], "sparql_test_on": ["edit"], "use_base_iris": true, "use_labels": true}`.


- **`robot_settings`**: Refer to *[#/definitions/CommandSettings](#definitions/CommandSettings)*. Settings to pass to ROBOT such as amount of memory to be used.


- **`robot_version`** *(string)* Only set this if you want to pin to a specific robot version.


- **`sssom_mappingset_group`**: Refer to *[#/definitions/SSSOMMappingSetGroup](#definitions/SSSOMMappingSetGroup)*. Block that includes information on all SSSOM mapping tables used.


- **`subset_group`**: Refer to *[#/definitions/SubsetGroup](#definitions/SubsetGroup)*. Block that includes information on all subsets (aka slims) to be generated.


- **`title`** *(string)*: Concise descriptive text about this ontology. Default: `""`.


- **`travis_emails`** *(list)* Emails to use in travis configurations. 
  - **Items** *(string)*


- **`uribase`** *(string)*: Base URI for PURLs. For an example see https://gitlab.c-path.org/c-pathontology/critical-path-ontology. Default: `"http://purl.obolibrary.org/obo"`.


- **`uribase_suffix`** *(string)* Suffix for the uri base. If not set, the suffix will be the ontology id by default.


- **`use_context`** *(boolean)*: If True, a context file is created that allows the user to specify prefixes used across the project. Default: `false`.


- **`use_custom_import_module`** *(boolean)*: if true add a custom import module which is managed through a robot template. This can also be used to manage your module seed. Default: `false`.


- **`use_dosdps`** *(boolean)*: if true use dead simple owl design patterns. Default: `false`.


- **`use_edit_file_imports`** *(boolean)*: If True, ODK will release the ontology with imports explicitly specified by owl:imports in the edit file.
    If False, ODK will build and release the ontology with _all_ imports and _all_ components specified in the ODK config file. Default: `true`.


- **`use_env_file_docker`** *(boolean)*: if true environment variables are collected by the docker wrapper and passed into the container. Default: `false`.


- **`use_external_date`** *(boolean)*: Flag to set if you want odk to use the host `date` rather than the docker internal `date`. Default: `false`.


- **`use_mappings`** *(boolean)*: if true use SSSOM mapping files. Default: `false`.


- **`use_templates`** *(boolean)*: if true use ROBOT templates. Default: `false`.


- **`workflows`** *(list)*: Workflows that are synced when updating the repo. Currently available: docs, diff, qc, release-diff. Default: `["docs"]`.
  - **Items** *(string)*
- <a id="definitions/CommandSettings"></a>**`CommandSettings`** *(object)*:     Settings to be provided to a tool like ROBOT    .
  - **`memory_gb`** *(integer)*
- <a id="definitions/ComponentGroup"></a>**`ComponentGroup`**:     A configuration section that consists of a list of `ComponentProduct` descriptions<br>      Controls extraction of import modules via robot extract into the "components/" directory    .
  - **All of**
    - : Refer to *[#/definitions/ComponentProduct](#definitions/ComponentProduct)*.
    - *object*
      - **`directory`** *(string)*: Default: `"components"`.
      - **`products`** *(list)*
        - **Items**: Refer to *[#/definitions/ComponentProduct](#definitions/ComponentProduct)*.
- <a id="definitions/ComponentProduct"></a>**`ComponentProduct`** *(object)*:     Represents an individual component    Examples: a file external to the edit file that contains axioms that belong to this ontology    Components are usually maintained manually.    .
  - **`base_iris`** *(list)*
    - **Items** *(string)*
  - **`filename`** *(string)*
  - **`make_base`** *(boolean)*: Default: `false`.
  - **`mappings`** *(list)*
    - **Items** *(string)*
  - **`source`** *(string)*
  - **`sssom_tool_options`** *(string)*: Default: `""`.
  - **`template_options`** *(string)*
  - **`templates`** *(list)*
    - **Items** *(string)*
  - **`use_mappings`** *(boolean)*: Default: `false`.
  - **`use_template`** *(boolean)*: Default: `false`.
- <a id="definitions/DocumentationGroup"></a>**`DocumentationGroup`** *(object)*:     Setting for the repos documentation system    .
  - **`documentation_system`** *(string)*: Default: `"mkdocs"`.
- <a id="definitions/ImportGroup"></a>**`ImportGroup`**:     A configuration section that consists of a list of `ImportProduct` descriptions<br>      Controls extraction of import modules via robot extract into the "imports/" directory    .
  - **All of**
    - : Refer to *[#/definitions/ProductGroup](#definitions/ProductGroup)*.
    - *object*
      - **`annotate_defined_by`** *(boolean)*: Default: `false`.
      - **`annotation_properties`** *(list)*: Default: `["rdfs:label", "IAO:0000115"]`.
        - **Items** *(string)*
      - **`base_merge_drop_equivalent_class_axioms`** *(boolean)*: Default: `true`.
      - **`directory`** *(string)*: Default: `"imports/"`.
      - **`exclude_iri_patterns`** *(list)*
        - **Items** *(string)*
      - **`export_obo`** *(boolean)*: Default: `false`.
      - **`mirror_max_time_download`** *(integer)*: Default: `200`.
      - **`mirror_retry_download`** *(integer)*: Default: `4`.
      - **`module_type`** *(string)*: Default: `"slme"`.
      - **`module_type_slme`** *(string)*: Default: `"BOT"`.
      - **`products`** *(list)*
        - **Items**: Refer to *[#/definitions/ImportProduct](#definitions/ImportProduct)*.
      - **`release_imports`** *(boolean)*: Default: `false`.
      - **`slme_individuals`** *(string)*: Default: `"include"`.
      - **`use_base_merging`** *(boolean)*: Default: `false`.
- <a id="definitions/ImportProduct"></a>**`ImportProduct`**:     Represents an individual import    Examples: 'uberon' (in go)    Imports are typically built from an upstream source, but this can be configured    .
  - **All of**
    - : Refer to *[#/definitions/Product](#definitions/Product)*.
    - *object*
      - **`annotation_properties`** *(list)*: Default: `["rdfs:label", "IAO:0000115"]`.
        - **Items** *(string)*
      - **`base_iris`** *(list)*
        - **Items** *(string)*
      - **`is_large`** *(boolean)*: Default: `false`.
      - **`make_base`** *(boolean)*: Default: `false`.
      - **`mirror_from`** *(string)*
      - **`mirror_type`** *(string)*
      - **`module_type`** *(string)*
      - **`module_type_slme`** *(string)*: Default: `"BOT"`.
      - **`slme_individuals`** *(string)*: Default: `"include"`.
      - **`use_base`** *(boolean)*: Default: `false`.
      - **`use_gzipped`** *(boolean)*: Default: `false`.
- <a id="definitions/PatternPipelineGroup"></a>**`PatternPipelineGroup`**:     A configuration section that consists of a list of `PatternPipelineProduct` descriptions<br>      Controls the handling of patterns data in the "src/patterns/data" directory    .
  - **All of**
    - : Refer to *[#/definitions/ProductGroup](#definitions/ProductGroup)*.
    - *object*
      - **`directory`** *(string)*: Default: `"../patterns/"`.
      - **`matches`** *(list)*
        - **Items**: Refer to *[#/definitions/PatternPipelineProduct](#definitions/PatternPipelineProduct)*.
      - **`products`** *(list)*
        - **Items**: Refer to *[#/definitions/PatternPipelineProduct](#definitions/PatternPipelineProduct)*.
- <a id="definitions/PatternPipelineProduct"></a>**`PatternPipelineProduct`**:     Represents an individual pattern pipeline    Examples: manual curation pipeline, auto curation pipeline    Each pipeline gets their own specific directory    .
  - **All of**
    - : Refer to *[#/definitions/Product](#definitions/Product)*.
    - *object*
      - **`dosdp_tools_options`** *(string)*: Default: `"--obo-prefixes=true"`.
      - **`ontology`** *(string)*: Default: `"$(SRC)"`.
- <a id="definitions/Product"></a>**`Product`** *(object)*:     abstract base class for all products.<br>      Here, a product is something that is produced by an ontology workflow.    A product can be manifested in different formats.        For example, goslim_prok is a subset (aka slim) product from GO,    this can be manifest as obo, owl, json    .
  - **`description`** *(string)*
  - **`id`** *(string, required)*
  - **`maintenance`** *(string)*: Default: `"manual"`.
  - **`rebuild_if_source_changes`** *(boolean)*: Default: `true`.
  - **`robot_settings`**: Refer to *[#/definitions/CommandSettings](#definitions/CommandSettings)*.
- <a id="definitions/ProductGroup"></a>**`ProductGroup`** *(object)*:     abstract base class for all product groups.<br>      A product group is a simple holder for a list of    groups, with the ability to set configurations that    hold by default for all within that group.<br>      Note: currently the configuration can specify    EITHER a list of ontology ids (e.g. uberon, cl)    OR a list of product objects    OR some mixture<br>      For example, in specifying upstream imports I can    be lazy and just list the ids, but if I need to    configure each one individually then I need to specify    the full product object.<br>      This buys some simplicity for the majority of projects    that don't do anything fancy, but at the price of overall    complexity    .
  - **`disabled`** *(boolean)*: Default: `false`.
  - **`ids`** *(list)*
    - **Items** *(string)*
  - **`rebuild_if_source_changes`** *(boolean)*: Default: `true`.
- <a id="definitions/SSSOMMappingSetGroup"></a>**`SSSOMMappingSetGroup`** *(object)*:     A configuration section that consists of a list of `SSSOMMappingSetProduct` descriptions    .
  - **`directory`** *(string)*: Default: `"../mappings"`.
  - **`products`** *(list)*
    - **Items**: Refer to *[#/definitions/SSSOMMappingSetProduct](#definitions/SSSOMMappingSetProduct)*.
  - **`release_mappings`** *(boolean)*: Default: `false`.
- <a id="definitions/SSSOMMappingSetProduct"></a>**`SSSOMMappingSetProduct`**:     Represents an SSSOM Mapping template template    .
  - **All of**
    - : Refer to *[#/definitions/Product](#definitions/Product)*.
    - *object*
      - **`mirror_from`** *(string)*
      - **`source_file`** *(string)*
      - **`sssom_tool_options`** *(string)*: Default: `""`.
- <a id="definitions/SubsetGroup"></a>**`SubsetGroup`**:     A configuration section that consists of a list of `SubsetProduct` descriptions<br>      Controls export of subsets/slims into the "subsets/" directory    .
  - **All of**
    - : Refer to *[#/definitions/ProductGroup](#definitions/ProductGroup)*.
    - *object*
      - **`directory`** *(string)*: Default: `"subsets/"`.
      - **`products`** *(list)*
        - **Items**: Refer to *[#/definitions/SubsetProduct](#definitions/SubsetProduct)*.
- <a id="definitions/SubsetProduct"></a>**`SubsetProduct`**:     Represents an individual subset.    Examples: goslim_prok (in go), eco_subset (in ro)    .
  - **All of**
    - : Refer to *[#/definitions/Product](#definitions/Product)*.
    - *object*
      - **`creators`** *(list)*
        - **Items** *(string)*


