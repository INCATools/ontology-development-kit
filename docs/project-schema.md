
## ODK Project Configuration Schema

- **`allow_equivalents`** *(string)*: can be all, none or asserted-only (see ROBOT documentation: http://robot.obolibrary.org/reason). Default: `all`.


- **`catalog_file`** *(string)*: Name of the catalog file to be used by the build. Default: `catalog-v001.xml`.


- **`ci`** *(list)*: continuous integration defaults; currently available: travis, github_actions. Default: `['github_actions']`.
  - **Items** *(string)*


- **`components`**:
    - **`filename`** *(string)* The filename of this component.
    - **`source`** *(string)* The source for which the component should be obtained.
    - **`directory`** *(string)*: directory where components are maintained. Default: `components`.
    - **`products`** *(list)*
        - **`filename`** *(string)* The filename of this component.
        - **`source`** *(string)* The source for which the component should be obtained.


- **`contact`** *(string)* Single contact for ontology as required by OBO.


- **`contributors`** *(list)* List of ontology contributors (currently setting this has no effect).
  - **Items** *(string)*


- **`create_obo_metadata`** *(boolean)*: if true OBO Markdown and PURL configs are created. Default: `True`.


- **`creators`** *(list)* List of ontology creators (currently setting this has no effect).
  - **Items** *(string)*


- **`custom_makefile_header`** *(string)*: A multiline string that is added to the Makefile. Default: `# ----------------------------------------# More information: https://github.com/INCATools/ontology-development-kit/`.


- **`description`** *(string)*: Provide a short description of the ontology. Default: `None`.


- **`documentation`**:
    - **`documentation_system`** *(string)*: Currently, only mkdocs is supported.  Default: `mkdocs`.


- **`dosdp_tools_options`** *(string)*: default parameters for dosdp-tools. Default: `--obo-prefixes=true`.


- **`edit_format`** *(string)*: Format in which the edit file is managed, either obo or owl. Default: `owl`.


- **`exclude_tautologies`** *(string)*: Remove tautologies such as A SubClassOf: owl:Thing or owl:Nothing SubclassOf: A. For more information see http://robot.obolibrary.org/reason#excluding-tautologies. Default: `structural`.


- **`export_formats`** *(list)*: A list of export formats you wish your release artefacts to be exported to, such as owl, obo, gz, ttl. Default: `['owl', 'obo']`.
  - **Items** *(string)*


- **`export_project_yaml`** *(boolean)*: Flag to set if you want a full project.yaml to be exported, including all the default options. Default: `False`.


- **`git_main_branch`** *(string)*: The main branch for your repo, such as main, or (now discouraged) master. Default: `main`.


- **`git_user`** *(string)*: GIT user name (necessary for generating releases). Default: ``.


- **`github_org`** *(string)*: Name of github org or username where repo will live. Examples: obophenotype, cmungall. Default: ``.


- **`gzip_main`** *(boolean)*: if true add a gzipped version of the main artefact. Default: `False`.


- **`id`** *(string)*: OBO id for this ontology. Must be lowecase Examples: uberon, go, cl, envo, chebi. Default: ``.


- **`import_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `False`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `True`.
    - **`annotation_properties`** *(list)*: Define which annotation properties to pull in. Default: `['rdfs:label', 'IAO:0000115']`.
    - **`directory`** *(string)*: directory where imports are extracted into to. Default: `imports/`.
    - **`module_type`** *(string)*: Module type. Supported: slme, minimal, custom. Default: `slme`.
    - **`module_type_slme`** *(string)*: SLME module type. Supported: BOT, TOP, STAR. Default: `BOT`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`annotation_properties`** *(list)*: Define which annotation properties to pull in. Default: `['rdfs:label', 'IAO:0000115']`.
        - **`base_iris`** *(list)*: if specified this URL is used rather than the default OBO PURL for the main OWL product. Default: ``.
        - **`is_large`** *(boolean)*: if large, ODK may take measures to reduce the memory footprint of the import. Default: `False`.
        - **`mirror_from`** *(string)*: if specified this URL is used rather than the default OBO PURL for the main OWL product. Default: ``.
        - **`module_type`** *(string)*: Module type. Supported: slme, minimal, custom. Default: ``.
        - **`module_type_slme`** *(string)*: SLME module type. Supported: BOT, TOP, STAR. Default: `BOT`.
        - **`slme_individuals`** *(string)*: See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme. Default: `include`.
        - **`use_base`** *(boolean)*: if use_base is true, try use the base IRI instead of normal one to mirror from. Default: `False`.
        - **`use_gzipped`** *(boolean)*: if use_gzipped is true, try use the base IRI instead of normal one to mirror from. Default: `False`.
    - **`release_imports`** *(boolean)*: If set to True, imports are copied to the release directory. Default: `False`.
    - **`slme_individuals`** *(string)*: See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme. Default: `include`.


- **`import_pattern_ontology`** *(boolean)*: if true import pattern.owl. Default: `False`.


- **`license`** *(string)*: Which license is ontology supplied under - must be an IRI. Default: `https://creativecommons.org/licenses/unspecified`.


- **`namespaces`** *(list)* A list of namespaces that are considered at home in this ontology. Used for certain filter commands.
  - **Items** *(string)*


- **`obo_format_options`** *(string)*: Additional args to pass to robot when saving to obo. TODO consider changing to a boolean for checks. Default: ``.


- **`pattern_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `False`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `True`.
    - **`directory`** *(string)*: directory where pattern source lives, also where TSV exported to. Default: `../patterns/`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.


- **`pattern_pipelines_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `False`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `True`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`dosdp_tools_options`** *(string)*: Default: `--obo-prefixes=true`.


- **`primary_release`** *(string)*: Which release file should be published as the primary release artefact, i.e. foo.owl. Default: `full`.


- **`public_release`** *(string)*: if true add functions to run automated releases (experimental). Current options are: github_curl, github_python. Default: `none`.


- **`public_release_assets`** *(list)* A list of files that gets added to a github/gitlab/etc release (as assets). If this option is not set (None), the standard ODK assets will be deployed.
  - **Items** *(string)*


- **`reasoner`** *(string)*: Name of reasoner to use in ontology pipeline, see robot reason docs for allowed values. Default: `ELK`.


- **`release_artefacts`** *(list)*: A list of release artefacts you wish to be exported. Default: `['full', 'base']`.
  - **Items** *(string)*


- **`release_date`** *(boolean)*: if true, releases will be tagged with a release date (oboInOwl:date). Default: `False`.


- **`remove_owl_nothing`** *(boolean)*: Flag to set if you want odk to remove owl:Nothing from releases. Default: `False`.


- **`repo`** *(string)*: Name of repo (do not include org). E.g. cell-ontology. Default: ``.


- **`robot_java_args`** *(string)*: Java args to pass to ROBOT at runtime, such as -Xmx6G. Default: ``.


- **`robot_report`** *(object)*: Block that includes settings for ROBOT report, ROBOT verify and additional reports that are generated. Default: `{'custom_profile': False, 'custom_sparql_checks': ['equivalent-classes', 'owldef-self-reference'], 'custom_sparql_exports': ['basic-report', 'class-count-by-prefix', 'edges', 'xrefs', 'obsoletes', 'synonyms'], 'ensure_owl2dl_profile': True, 'fail_on': None, 'release_reports': False, 'report_on': ['edit'], 'use_labels': True}`.


- **`robot_settings`**:
    - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.


- **`robot_version`** *(string)* Only set this if you want to pin to a specific robot version.


- **`robotemplate_group`**:
    - **`directory`** *(string)*: Default: `../templates/`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `True`.
        - **`robot_settings`**:
          - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.


- **`subset_group`**:
    - **`disabled`** *(boolean)*: if set then this is not used. Default: `False`.
    - **`ids`** *(list)* potentially deprecated, specify explicit product list instead.
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: if false then upstream ontology is re-downloaded any time edit file changes. Default: `True`.
    - **`directory`** *(string)*: directory where subsets are placed after extraction from ontology. Default: `subsets/`.
    - **`products`** *(list)*
        - **`description`** *(string)* A concise textual description of the product.
        - **`id`** *(string)* ontology project identifier / shorthand; e.g. go, obi, envo.
        - **`rebuild_if_source_changes`** *(boolean)*: If false then previously downloaded versions of external ontologies are used. Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)* Amount of memory in GB to provide for tool such as robot.
        - **`creators`** *(list)*: list of people that are credited as creators/maintainers of the subset. Default: ``.


- **`title`** *(string)*: Concise descriptive text about this ontology. Default: ``.


- **`travis_emails`** *(list)* Emails to use in travis configurations. 
  - **Items** *(string)*


- **`uribase`** *(string)*: Base URI for PURLs. DO NOT MODIFY AT THIS TIME, code is still hardwired for OBO. Default: `http://purl.obolibrary.org/obo`.


- **`use_custom_import_module`** *(boolean)*: if true add a custom import module which is managed through a robot template. This can also be used to manage your module seed. Default: `False`.


- **`use_dosdps`** *(boolean)*: if true use dead simple owl design patterns. Default: `False`.


- **`use_external_date`** *(boolean)*: Flag to set if you want odk to use the host `date` rather than the docker internal `date`. Default: `False`.


