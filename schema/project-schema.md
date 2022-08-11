
## ODK Project Schema

- **`allow_equivalents`** *(string)*: Default: `all`.


- **`catalog_file`** *(string)*: Default: `catalog-v001.xml`.


- **`ci`** *(list)*: Default: `['github_actions']`.
  - **Items** *(string)*


- **`components`**:
    - **`filename`** *(string)*
    - **`source`** *(string)*
    - **`directory`** *(string)*: Default: `components`.
    - **`products`** *(list)*
        - **`filename`** *(string)*
        - **`source`** *(string)*


- **`contact`** *(string)*


- **`contributors`** *(list)*
  - **Items** *(string)*


- **`create_obo_metadata`** *(boolean)*: Default: `True`.


- **`creators`** *(list)*
  - **Items** *(string)*


- **`custom_makefile_header`** *(string)*: Default: `# ----------------------------------------# More information: https://github.com/INCATools/ontology-development-kit/`.


- **`description`** *(string)*: Default: `None`.


- **`documentation`**:
    - **`documentation_system`** *(string)*: Default: `mkdocs`.


- **`dosdp_tools_options`** *(string)*: Default: `--obo-prefixes=true`.


- **`edit_format`** *(string)*: Default: `owl`.


- **`exclude_tautologies`** *(string)*: Default: `structural`.


- **`export_formats`** *(list)*: Default: `['owl', 'obo']`.
  - **Items** *(string)*


- **`export_project_yaml`** *(boolean)*: Default: `False`.


- **`git_main_branch`** *(string)*: Default: `main`.


- **`git_user`** *(string)*: Default: ``.


- **`github_org`** *(string)*: Default: ``.


- **`gzip_main`** *(boolean)*: Default: `False`.


- **`id`** *(string)*: Default: ``.


- **`import_group`**:
    - **`disabled`** *(boolean)*: Default: `False`.
    - **`ids`** *(list)*
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
    - **`annotation_properties`** *(list)*: Default: `['rdfs:label', 'IAO:0000115']`.
    - **`directory`** *(string)*: Default: `imports/`.
    - **`module_type`** *(string)*: Default: `slme`.
    - **`module_type_slme`** *(string)*: Default: `BOT`.
    - **`products`** *(list)*
        - **`description`** *(string)*
        - **`id`** *(string)*
        - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)*
        - **`annotation_properties`** *(list)*: Default: `['rdfs:label', 'IAO:0000115']`.
        - **`base_iris`** *(list)*: Default: ``.
        - **`is_large`** *(boolean)*: Default: `False`.
        - **`mirror_from`** *(string)*: Default: ``.
        - **`module_type`** *(string)*: Default: ``.
        - **`module_type_slme`** *(string)*: Default: `BOT`.
        - **`slme_individuals`** *(string)*: Default: `include`.
        - **`use_base`** *(boolean)*: Default: `False`.
        - **`use_gzipped`** *(boolean)*: Default: `False`.
    - **`release_imports`** *(boolean)*: Default: `False`.
    - **`slme_individuals`** *(string)*: Default: `include`.


- **`import_pattern_ontology`** *(boolean)*: Default: `False`.


- **`license`** *(string)*: Default: `https://creativecommons.org/licenses/unspecified`.


- **`namespaces`** *(list)*
  - **Items** *(string)*


- **`obo_format_options`** *(string)*: Default: ``.


- **`pattern_group`**:
    - **`disabled`** *(boolean)*: Default: `False`.
    - **`ids`** *(list)*
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
    - **`directory`** *(string)*: Default: `../patterns/`.
    - **`products`** *(list)*
        - **`description`** *(string)*
        - **`id`** *(string)*
        - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)*


- **`pattern_pipelines_group`**:
    - **`disabled`** *(boolean)*: Default: `False`.
    - **`ids`** *(list)*
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
    - **`products`** *(list)*
        - **`description`** *(string)*
        - **`id`** *(string)*
        - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)*
        - **`dosdp_tools_options`** *(string)*: Default: `--obo-prefixes=true`.


- **`primary_release`** *(string)*: Default: `full`.


- **`public_release`** *(string)*: Default: `none`.


- **`public_release_assets`** *(list)*
  - **Items** *(string)*


- **`reasoner`** *(string)*: Default: `ELK`.


- **`release_artefacts`** *(list)*: Default: `['full', 'base']`.
  - **Items** *(string)*


- **`release_date`** *(boolean)*: Default: `False`.


- **`remove_owl_nothing`** *(boolean)*: Default: `False`.


- **`repo`** *(string)*: Default: ``.


- **`robot_java_args`** *(string)*: Default: ``.


- **`robot_report`** *(object)*: Default: `{'custom_profile': False, 'custom_sparql_checks': ['equivalent-classes', 'owldef-self-reference'], 'custom_sparql_exports': ['basic-report', 'class-count-by-prefix', 'edges', 'xrefs', 'obsoletes', 'synonyms'], 'ensure_owl2dl_profile': False, 'fail_on': None, 'release_reports': False, 'report_on': ['edit'], 'use_labels': True}`.


- **`robot_settings`**:
    - **`memory_gb`** *(integer)*


- **`robot_version`** *(string)*


- **`robotemplate_group`**:
    - **`directory`** *(string)*: Default: `../templates/`.
    - **`products`** *(list)*
        - **`description`** *(string)*
        - **`id`** *(string)*
        - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
        - **`robot_settings`**:
          - **`memory_gb`** *(integer)*


- **`subset_group`**:
    - **`disabled`** *(boolean)*: Default: `False`.
    - **`ids`** *(list)*
      - **Items** *(string)*
    - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
    - **`directory`** *(string)*: Default: `subsets/`.
    - **`products`** *(list)*
        - **`description`** *(string)*
        - **`id`** *(string)*
        - **`rebuild_if_source_changes`** *(boolean)*: Default: `True`.
        - **`robot_settings`**:
            - **`memory_gb`** *(integer)*
        - **`creators`** *(list)*: Default: ``.


- **`title`** *(string)*: Default: ``.


- **`travis_emails`** *(list)*
  - **Items** *(string)*


- **`uribase`** *(string)*: Default: `http://purl.obolibrary.org/obo`.


- **`use_custom_import_module`** *(boolean)*: Default: `False`.


- **`use_dosdps`** *(boolean)*: Default: `False`.


- **`use_external_date`** *(boolean)*: Default: `False`.


