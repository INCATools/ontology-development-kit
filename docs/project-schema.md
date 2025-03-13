
## ODK Project Configuration Schema

- **`allow_equivalents`** *(string)*: can be all, none or asserted-only (see ROBOT documentation: http://robot.obolibrary.org/reason). Default: `"asserted-only"`.


- **`catalog_file`** *(string)*: Name of the catalog file to be used by the build. Default: `"catalog-v001.xml"`.


- **`ci`** *(list)*: continuous integration defaults; currently available: travis, github_actions, gitlab-ci. Default: `["github_actions"]`.
  - **Items** *(string)*


- **`components`**:
    - **`base_iris`** *(list)* A list of URI prefixes used to identify terms belonging to the component.
      - **Items** *(string)*
    - **`filename`** *(string)* The filename of this component.
    - **`make_base`** *(boolean)*: if make_base is true, the file is turned into a base (works with `source`). Default: `false`.
    - **`mappings`** *(list)* A list of SSSOM template names. If set, these will be used to source this component.
      - **Items** *(string)*
    - **`source`** *(string)* The URL source for which the component should be obtained.
    - **`sssom_tool_options`** *(string)*: SSSOM toolkit options passed to the sssom command used to generate this product command. Default: `""`.
    - **`template_options`** *(string)* ROBOT options passed to the template command.
    - **`templates`** *(list)* A list of ROBOT template names. If set, these will be used to source this component.
      - **Items** *(string)*
    - **`use_mappings`** *(boolean)*: If true, the component will be sourced from one or more SSSOM mapping files. Default: `false`.
    - **`use_template`** *(boolean)*: If true, the component will be sourced by a template. Default: `false`.
    - **`directory`** *(string)*: directory where components are maintained. Default: `components`.
    - **`products`** *(list)*
        - **`base_iris`** *(list)* A list of URI prefixes used to identify terms belonging to the component.
          - **Items** *(string)*
        - **`filename`** *(string)* The filename of this component.
        - **`make_base`** *(boolean)*: if make_base is true, the file is turned into a base (works with `source`). Default: `false`.
        - **`mappings`** *(list)* A list of SSSOM template names. If set, these will be used to source this component.
          - **Items** *(string)*
        - **`source`** *(string)* The URL source for which the component should be obtained.
        - **`sssom_tool_options`** *(string)*: SSSOM toolkit options passed to the sssom command used to generate this product command. Default: `""`.
        - **`template_options`** *(string)* ROBOT options passed to the template command.
        - **`templates`** *(list)* A list of ROBOT template names. If set, these will be used to source this component.
          - **Items** *(string)*
        - **`use_mappings`** *(boolean)*: If true, the component will be sourced from one or more SSSOM mapping files. Default: `false`.
        - **`use_template`** *(boolean)*: If true, the component will be sourced by a template. Default: `false`.


- **`contact`** *(string)* Single contact for ontology as required by OBO.


- **`contributors`** *(list)* List of ontology contributors (currently setting this has no effect).
  - **Items** *(string)*


- **`create_obo_metadata`** *(boolean)*: if true OBO Markdown and PURL configs are created. Default: `true`.


- **`creators`** *(list)* List of ontology creators (currently setting this has no effect).
  - **Items** *(string)*


- **`custom_makefile_header`** *(string)*: A multiline string that is added to the Makefile. Default: `"\n# ----------------------------------------\n# More information: https://github.com/INCATools/ontology-development-kit/\n"`.


- **`description`** *(string)*: Provide a short description of the ontology. Default: `"None"`.


- **`documentation`**:
    - **`documentation_system`** *(string)*: Currently, only mkdocs is supported.  Default: `"mkdocs"`.


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


- **`id`** *(string)*: OBO id for this ontology. Must be lowercase Examples: uberon, go, cl, envo, chebi. Default: `""`.


- **`import_component_format`** *(string)*: The default serialisation for all components and imports. Default: `"ofn"`.


- **`import_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `false`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `true`.
    - **`annotate_defined_by`** *(boolean)*: If set to true, the annotation rdfs:definedBy is added for each external class. 
       In the case of use_base_merging is also true, this will be added to the imports/merged_import.owl file.
       When imports are not merged, the annotation is added during the release process to the full release artefact.
     Default: `False`.
    - **`annotation_properties`** *(list)*: Define which annotation properties to pull in. Default: `['rdfs:label', 'IAO:0000115']`.
    - **`base_merge_drop_equivalent_class_axioms`** *(boolean)*: If set to true, equivalent class axioms will be removed before extracting a module with the base-merging process. Default: `True`.
    - **`directory`** *(string)*: directory where imports are extracted into to. Default: `imports/`.
    - **`exclude_iri_patterns`** *(list)*: List of IRI patterns. If set, IRIs matching and IRI pattern will be removed from the import. Default: ``.
    - **`export_obo`** *(boolean)*: If set to true, modules will not only be created in OWL, but also OBO format. Default: `False`.
    - **`mirror_max_time_download`** *(integer)*: Corresponds to the cURL --max-time parameter (in seconds), see http://www.ipgp.fr/~arnaudl/NanoCD/software/win32/curl/docs/curl.html. Default: `200`.
    - **`mirror_retry_download`** *(integer)*: Corresponds to the cURL --retry parameter, see http://www.ipgp.fr/~arnaudl/NanoCD/software/win32/curl/docs/curl.html. Default: `4`.
    - **`module_type`** *(string)*: Module type. Supported: slme, minimal, custom. Default: `slme`.
    - **`module_type_slme`** *(string)*: SLME module type. Supported: BOT, TOP, STAR. Default: `BOT`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string, required)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`maintenance`** *(string)*: A setting that can be used to change certain assets that are typically managed automatically (by ODK) to manual or other maintenance strategies. Default: `"manual"`.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `true`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`annotation_properties`** *(list)*: Define which annotation properties to pull in. Default: `['rdfs:label', 'IAO:0000115']`.
        - **`base_iris`** *(list)*: if specified this URL is used rather than the default OBO PURL for the main OWL product. Default: ``.
        - **`is_large`** *(boolean)*: if large, ODK may take measures to reduce the memory footprint of the import. Default: `False`.
        - **`make_base`** *(boolean)*: if make_base is true, try to extract a base file from the mirror. Default: `False`.
        - **`mirror_from`** *(string)*: if specified this URL is used rather than the default OBO PURL for the main OWL product. Default: ``.
        - **`mirror_type`** *(string)*: Define the type of the mirror for your import. Supported: base, custom, no_mirror. Default: ``.
        - **`module_type`** *(string)*: Module type. Supported: slme, minimal, custom, mirror. Default: ``.
        - **`module_type_slme`** *(string)*: SLME module type. Supported: BOT, TOP, STAR. Default: `BOT`.
        - **`slme_individuals`** *(string)*: See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme. Default: `include`.
        - **`use_base`** *(boolean)*: if use_base is true, try use the base IRI instead of normal one to mirror from. Default: `False`.
        - **`use_gzipped`** *(boolean)*: if use_gzipped is true, try use the base IRI instead of normal one to mirror from. Default: `False`.
    - **`release_imports`** *(boolean)*: If set to True, imports are copied to the release directory. Default: `False`.
    - **`slme_individuals`** *(string)*: See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme. Default: `include`.
    - **`use_base_merging`** *(boolean)*: If set to true, mirrors will be merged before determining a suitable seed. This can be a quite costly process. Default: `False`.


- **`import_pattern_ontology`** *(boolean)*: if true import pattern.owl. Default: `false`.


- **`license`** *(string)*: Which license is ontology supplied under - must be an IRI. Default: `"https://creativecommons.org/licenses/unspecified"`.


- **`namespaces`** *(list)* A list of namespaces that are considered at home in this ontology. Used for certain filter commands.
  - **Items** *(string)*


- **`obo_format_options`** *(string)*: Additional args to pass to robot when saving to obo. TODO consider changing to a boolean for checks. Default: `""`.


- **`owltools_memory`** *(string)*: OWLTools memory, for example 4GB. Default: `""`.


- **`pattern_pipelines_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `false`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `true`.
    - **`directory`** *(string)*: directory where pattern source lives, also where TSV exported to. Default: `../patterns/`.
    - **`matches`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string, required)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`maintenance`** *(string)*: A setting that can be used to change certain assets that are typically managed automatically (by ODK) to manual or other maintenance strategies. Default: `"manual"`.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `true`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`dosdp_tools_options`** *(string)*: Default: `--obo-prefixes=true`.
        - **`ontology`** *(string)*: Default: `$(SRC)`.
    - **`products`** *(list)*
      - ...


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
    reason (the classification/subclassOf hierarchy computation); materialize (the materialisation of simple existential/
    object property restrictions); reduce (the removal of redundant subclassOf axioms). Default: `true`.


- **`remove_owl_nothing`** *(boolean)*: Flag to set if you want odk to remove owl:Nothing from releases. Default: `false`.


- **`repo`** *(string)*: Name of repo (do not include org). E.g. cell-ontology. Default: `""`.


- **`robot_java_args`** *(string)*: Java args to pass to ROBOT at runtime, such as -Xmx6G. Default: `""`.


- **`robot_report`** *(object)*: Block that includes settings for ROBOT report, ROBOT verify and additional reports that are generated. Default: `{"custom_profile": false, "custom_sparql_checks": ["owldef-self-reference", "iri-range", "label-with-iri", "multiple-replaced_by", "dc-properties"], "custom_sparql_exports": ["basic-report", "class-count-by-prefix", "edges", "xrefs", "obsoletes", "synonyms"], "ensure_owl2dl_profile": true, "fail_on": null, "release_reports": false, "report_on": ["edit"], "sparql_test_on": ["edit"], "use_base_iris": true, "use_labels": true}`.


- **`robot_settings`**:
    - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.


- **`robot_version`** *(string)* Only set this if you want to pin to a specific robot version.


- **`sssom_mappingset_group`**:
    - **`directory`** *(string)*: Default: `"../mappings"`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string, required)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`maintenance`** *(string)*: A setting that can be used to change certain assets that are typically managed automatically (by ODK) to manual or other maintenance strategies. Default: `"manual"`.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `true`.
        - **`robot_settings`**:
          - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
      - **`mirror_from`** *(string)*: if specified this URL is used to mirror the mapping set. Default: ``.
      - **`source_file`** *(string)*: The name of the file from which the mappings should be extracted. Default: ``.
      - **`sssom_tool_options`** *(string)*: SSSOM toolkit options passed to the sssom command used to generate this product command. Default: ``.
    - **`release_mappings`** *(boolean)*: If set to True, mappings are copied to the release directory. Default: `false`.


- **`subset_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `false`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `true`.
    - **`directory`** *(string)*: directory where subsets are placed after extraction from ontology. Default: `subsets/`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string, required)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`maintenance`** *(string)*: A setting that can be used to change certain assets that are typically managed automatically (by ODK) to manual or other maintenance strategies. Default: `"manual"`.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `true`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`creators`** *(list)*: list of people that are credited as creators/maintainers of the subset. Default: ``.


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


