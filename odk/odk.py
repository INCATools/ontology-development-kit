#!/usr/bin/env python3
"""
Generate artefacts (Makefile, default ontology edit file, imports) from a project configuration

See https://github.com/ontodev/robot/issues/37

For help on command line usage:

odk.py 

"""
from typing import Optional, Set, List, Union, Dict, Any
import json
from dataclasses import dataclass, field
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_json import dataclass_json
from jinja2 import Template
from dacite import from_dict
import yaml
import os
import glob
import fnmatch
import subprocess
import shutil
from shutil import copy, copymode
import logging
from hashlib import sha256
from xml.etree import ElementTree
from defusedxml import ElementTree as DefusedElementTree

logging.basicConfig(level=logging.INFO)
TEMPLATE_SUFFIX = '.jinja2'

# Primitive Types
OntologyHandle = str ## E.g. uberon, cl; also subset names
Person = str ## ORCID or github handle
Email = str ## must be of NAME@DOMAIN form
Url = str
Directory = str

@dataclass_json
@dataclass
class CommandSettings(JsonSchemaMixin):
    """
    Settings to be provided to a tool like ROBOT
    """
    memory_gb : Optional[int] = None
    """Amount of memory in GB to provide for tool such as robot"""

@dataclass_json
@dataclass
class Product(JsonSchemaMixin):
    """
    abstract base class for all products.

    Here, a product is something that is produced by an ontology workflow.
    A product can be manifested in different formats.
    
    For example, goslim_prok is a subset (aka slim) product from GO,
    this can be manifest as obo, owl, json
    """
    
    id : str
    """ontology project identifier / shorthand; e.g. go, obi, envo"""
    
    description: Optional[str] = None
    """A concise textual description of the product"""
    
    maintenance: str = "manual"
    """A setting that can be used to change certain assets that are typically managed automatically (by ODK) to manual or other maintenance strategies."""
    
    rebuild_if_source_changes : bool = True
    """If false then previously downloaded versions of external ontologies are used"""
    
    robot_settings : Optional[CommandSettings] = None
    """Amount of memory to provide for robot. Working with large products such as CHEBI imports may require additional memory"""

@dataclass_json
@dataclass
class SubsetProduct(Product):
    """
    Represents an individual subset.
    Examples: goslim_prok (in go), eco_subset (in ro)
    """
    
    creators : Optional[List[Person]] = None
    """list of people that are credited as creators/maintainers of the subset"""

@dataclass_json
@dataclass
class ComponentProduct(JsonSchemaMixin):
    """
    Represents an individual component
    Examples: a file external to the edit file that contains axioms that belong to this ontology
    Components are usually maintained manually.
    """
    
    filename: Optional[str] = None
    """The filename of this component"""
    
    source: Optional[str] = None
    """The URL source for which the component should be obtained."""
    
    use_template: bool = False
    """If true, the component will be sourced by a template"""

    use_mappings: bool = False
    """If true, the component will be sourced from one or more SSSOM mapping files"""
    
    template_options: Optional[str] = None
    """ROBOT options passed to the template command"""

    sssom_tool_options: Optional[str] = ""
    """SSSOM toolkit options passed to the sssom command used to generate this product command"""
    
    templates: Optional[List[str]] = None
    """A list of ROBOT template names. If set, these will be used to source this component."""

    mappings: Optional[List[str]] = None
    """A list of SSSOM template names. If set, these will be used to source this component."""
    
    base_iris: Optional[List[str]] = None
    """A list of URI prefixes used to identify terms belonging to the component."""
    
    make_base: bool = False
    """if make_base is true, the file is turned into a base (works with `source`)."""

@dataclass_json
@dataclass
class ImportProduct(Product):
    """
    Represents an individual import
    Examples: 'uberon' (in go)
    Imports are typically built from an upstream source, but this can be configured
    """
    
    mirror_from: Optional[Url] = None
    """if specified this URL is used rather than the default OBO PURL for the main OWL product"""
    
    base_iris: Optional[List[str]] = None
    """if specified this URL is used rather than the default OBO PURL for the main OWL product"""
    
    is_large: bool = False
    """if large, ODK may take measures to reduce the memory footprint of the import."""
    
    module_type : Optional[str] = None
    """Module type. Supported: slme, minimal, custom, mirror"""
    
    module_type_slme : Optional[str] = None
    """SLME module type. Supported: BOT, TOP, STAR"""
    
    annotation_properties : List[str] = field(default_factory=lambda: ['rdfs:label', 'IAO:0000115', 'OMO:0002000'])
    """Define which annotation properties to pull in."""
    
    slme_individuals : Optional[str] = None
    """See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme"""
    
    use_base: bool = False
    """if use_base is true, try use the base IRI instead of normal one to mirror from."""
    
    make_base: bool = False
    """if make_base is true, try to extract a base file from the mirror."""
    
    use_gzipped: bool = False
    """if use_gzipped is true, try use the base IRI instead of normal one to mirror from."""

    mirror_type: Optional[str] = None
    """Define the type of the mirror for your import. Supported: base, custom, no_mirror."""

@dataclass_json
@dataclass
class PatternPipelineProduct(Product):
    """
    Represents an individual pattern pipeline
    Examples: manual curation pipeline, auto curation pipeline
    Each pipeline gets their own specific directory
    """
    dosdp_tools_options: str = "--obo-prefixes=true"
    ontology: str = "$(SRC)"

@dataclass_json
@dataclass
class SSSOMMappingSetProduct(Product):
    """
    Represents an SSSOM Mapping template template
    """
    mirror_from: Optional[Url] = None
    """if specified this URL is used to mirror the mapping set."""

    source_file: Optional[str] = None
    """The name of the file from which the mappings should be extracted"""

    sssom_tool_options: Optional[str] = ""
    """SSSOM toolkit options passed to the sssom command used to generate this product command"""

    release_mappings: bool = False
    """If set to True, this mapping set is treated as an artifact to be released."""

    source_mappings: Optional[List[str]] = None
    """The mapping sets to merge to create this product."""

@dataclass_json
@dataclass
class BabelonTranslationProduct(Product):
    """
    Represents a Babelon Translation
    """
    mirror_babelon_from: Optional[Url] = None
    """if specified this URL is used to mirror the translation."""
    
    mirror_synonyms_from: Optional[Url] = None
    """if specified this URL is used to mirror the synonym template from."""
    
    include_robot_template_synonyms: bool = False
    """if include_robot_template_synonyms is true, a ROBOT template synonym table is added in addition to the babelon translation table."""

    babelon_tool_options: Optional[str] = ""
    """Babelon toolkit options passed to the command used to generate this product command"""
    
    language: str = "en"
    """Language tag (IANA/ISO), e.g 'en', 'fr'."""
    
    include_not_translated: bool = False
    """if include_not_translated is 'false' NOT_TRANSLATED values are removed during preprocessing."""
    
    update_translation_status: bool = True
    """if update_translation_status is 'true', translations where the source_value has changed are relegated to CANDIDATE status."""
    
    drop_unknown_columns: bool = True
    """if drop_unknown_columns is 'true' columns that are not part of the babelon standard are removed during preprocessing."""
    
    auto_translate: bool = False
    """if auto_translate is true, missing values are being translated using the babelon toolkit during preprocessing. By default, the toolkit employs LLM-mediated translations using the OpenAI API. This default may change at any time."""

    

@dataclass_json
@dataclass
class ExportProduct(Product):
    """
    Represents a export product, such as one produced by a SPARQL query
    """
    
    method : str = "sparql"
    """How the export is generated. Currently only SPARQL is supported"""
    
    output_format : str = "tsv"
    """Output format, see robot query for details."""
    
    is_validation_check : bool = False
    """If true, then the presence of one or more results in query results in pipeline fail. Note these are in addition to the main robot report command"""

    export_specification: Optional[str] = None
    """Specification such as a SPARQL query. If unset, assumes a default path of ../sparql/{{id}}.sparql"""
    
    
@dataclass_json
@dataclass
class ProductGroup(JsonSchemaMixin):
    """
    abstract base class for all product groups.

    A product group is a simple holder for a list of
    groups, with the ability to set configurations that
    hold by default for all within that group.

    Note: currently the configuration can specify
    EITHER a list of ontology ids (e.g. uberon, cl)
    OR a list of product objects
    OR some mixture

    For example, in specifying upstream imports I can
    be lazy and just list the ids, but if I need to
    configure each one individually then I need to specify
    the full product object.

    This buys some simplicity for the majority of projects
    that don't do anything fancy, but at the price of overall
    complexity
    """
    
    ids : Optional[List[OntologyHandle]] = None
    """potentially deprecated, specify explicit product list instead"""
    
    disabled : bool = False
    """if set then this is not used"""
    
    rebuild_if_source_changes : bool = True
    """if false then upstream ontology is re-downloaded any time edit file changes"""

    def fill_missing(self, project):
        if self.products is None:
            self.products = []
        if self.ids is not None:
            for id in self.ids:
                if id not in [p.id for p in self.products]:
                    self._add_stub(id)
        self._derive_fields(project)

    def _derive_fields(self, project):
        pass

@dataclass_json
@dataclass
class SubsetGroup(ProductGroup):
    """
    A configuration section that consists of a list of `SubsetProduct` descriptions

    Controls export of subsets/slims into the "subsets/" directory
    """
    
    products : Optional[List[SubsetProduct]] = None
    """all subset products"""
    
    directory : Directory = "subsets/"
    """directory where subsets are placed after extraction from ontology"""
    
    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(SubsetProduct(id=id))

@dataclass_json
@dataclass
class ImportGroup(ProductGroup):
    """
    A configuration section that consists of a list of `ImportProduct` descriptions

    Controls extraction of import modules via robot extract into the "imports/" directory
    """
    
    products : Optional[List[ImportProduct]] = None
    """all import products"""
    
    module_type : str = "slme"
    """Module type. Supported: slme, minimal, custom"""
    
    module_type_slme : str = "BOT"
    """SLME module type. Supported: BOT, TOP, STAR"""
    
    slme_individuals : str = "include"
    """See http://robot.obolibrary.org/extract#syntactic-locality-module-extractor-slme"""
    
    mirror_retry_download : int = 4
    """Corresponds to the cURL --retry parameter, see http://www.ipgp.fr/~arnaudl/NanoCD/software/win32/curl/docs/curl.html"""
    
    mirror_max_time_download : int = 200
    """Corresponds to the cURL --max-time parameter (in seconds), see http://www.ipgp.fr/~arnaudl/NanoCD/software/win32/curl/docs/curl.html"""
    
    release_imports : bool = False
    """If set to True, imports are copied to the release directory."""
    
    use_base_merging: bool = False
    """If set to true, mirrors will be merged before determining a suitable seed. This can be a quite costly process."""
    
    base_merge_drop_equivalent_class_axioms: bool = False
    """If set to true, equivalent class axioms will be removed before extracting a module with the base-merging process. Do not activate this feature unless you are positive that your base merging process only leverages true base files, with asserted subclass axioms."""

    exclude_iri_patterns: Optional[List[str]] = None
    """List of IRI patterns. If set, IRIs matching and IRI pattern will be removed from the import."""
    
    export_obo: bool = False
    """If set to true, modules will not only be created in OWL, but also OBO format"""
    
    annotation_properties : List[str] = field(default_factory=lambda: ['rdfs:label', 'IAO:0000115', 'OMO:0002000'])
    """Define which annotation properties to pull in."""

    strip_annotation_properties: bool = True
    """If set to true, strip away annotation properties from imports, apart from explicitly imported properties and properties listed in annotation_properties."""
    
    directory : Directory = "imports/"
    """directory where imports are extracted into to"""
    
    annotate_defined_by : bool = False
    """If set to true, the annotation rdfs:definedBy is added for each external class. 
       In the case of use_base_merging is also true, this will be added to the imports/merged_import.owl file.
       When imports are not merged, the annotation is added during the release process to the full release artefact.
    """

    scan_signature : bool = True
    """If true, the edit file is scanned for additional terms to import.
       Otherwise, imports are seeded solely from the manually maintained
       *_terms.txt files. Note that setting this option to False makes
       Protégé-based declarations of terms to import impossible.
    """

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(ImportProduct(id=id))

    def _derive_fields(self, project):
        self.special_products = []
        for p in self.products:
            if p.module_type is None:
                # Use group-level module type
                p.module_type = self.module_type
            elif p.module_type == 'fast_slme':
                # Accept fast_slme as a synonym for slme, for backwards
                # compatibility
                p.module_type = 'slme'
            if p.module_type == 'slme':
                # Use group-level SLME parameters unless overriden
                if p.module_type_slme is None:
                    p.module_type_slme = self.module_type_slme
                if p.slme_individuals is None:
                    p.slme_individuals = self.slme_individuals
            if p.base_iris is None:
                p.base_iris = [ 'http://purl.obolibrary.org/obo/' + p.id.upper() ]
            if (p.is_large or p.module_type != self.module_type or
                (p.module_type == 'slme' and p.module_type_slme != self.module_type_slme)):
                # This module will require a distinct rule
                self.special_products.append(p)

@dataclass_json
@dataclass
class ReportConfig(JsonSchemaMixin):
    """
    A configuration section for ROBOT report
    """
    
    fail_on : Optional[str] = None
    """see http://robot.obolibrary.org/report#failing for details. """
    
    use_labels : bool = True
    """see http://robot.obolibrary.org/report#labels for details. """
    
    use_base_iris: bool = True
    """If true, only reports on problems with entities belonging to this ontology. Set the base_iris using the 'namespaces' at project level."""
    
    custom_profile : bool = False
    """This will replace the call to the standard OBO report to a custom profile instead."""
    
    report_on : List[str] = field(default_factory=lambda: ['edit'])
    """Chose which files to run the report on."""
    
    ensure_owl2dl_profile : bool = True
    """This will ensure that the main .owl release file conforms to the owl2 profile during make test."""
    
    release_reports : bool = False
    """ If true, release reports are added as assets to the release (top level directory, reports directory)"""
    
    custom_sparql_checks : Optional[List[str]] = field(default_factory=lambda: ['owldef-self-reference', 'iri-range', 'label-with-iri', 'multiple-replaced_by', 'dc-properties'])
    """ Chose which additional sparql checks you want to run. The related sparql query must be named CHECKNAME-violation.sparql, and be placed in the src/sparql directory.
        The custom sparql checks available are: 'owldef-self-reference', 'redundant-subClassOf', 'taxon-range', 'iri-range', 'iri-range-advanced', 'label-with-iri', 'multiple-replaced_by', 'term-tracker-uri', 'illegal-date', 'dc-properties'.
    """

    custom_sparql_exports : Optional[List[str]] = field(default_factory=lambda: ['basic-report', 'class-count-by-prefix', 'edges', 'xrefs', 'obsoletes', 'synonyms'])
    """Chose which custom reports to generate. The related sparql query must be named CHECKNAME.sparql, and be placed in the src/sparql directory."""

    sparql_test_on: List[str] = field(default_factory=lambda: ['edit'])
    """Chose which file to run the custom sparql checks. Supported 'edit', any release artefact."""

    upper_ontology: Optional[str] = None
    """IRI of an upper ontology to check the current ontology against."""

@dataclass_json
@dataclass
class DocumentationGroup(JsonSchemaMixin):
    """
    Setting for the repos documentation system
    """
    
    documentation_system : Optional[str] = 'mkdocs'
    """Currently, only mkdocs is supported. """
    
    

@dataclass_json
@dataclass
class ComponentGroup(ProductGroup):
    """
    A configuration section that consists of a list of `ComponentProduct` descriptions

    Controls extraction of import modules via robot extract into the "components/" directory
    """
    
    products : Optional[List[ComponentProduct]] = None
    """all component products"""

    directory : Directory = "components"
    """directory where components are maintained"""

    def _add_stub(self, filename : str):
        if self.products is None:
            self.products = []
        self.products.append(ComponentProduct(filename=filename))

    def _derive_fields(self, project):
        for product in self.products:
            if product.base_iris is None:
                product.base_iris = [project.uribase + '/' + project.id.upper()]
            if product.use_template and product.templates is None:
                product.templates = [product.filename.split('.')[0] + '.tsv']
            elif product.use_mappings and product.mappings is None:
                product.mappings = [product.filename.split('.')[0] + '.sssom.tsv']

@dataclass_json
@dataclass
class PatternPipelineGroup(ProductGroup):
    """
    A configuration section that consists of a list of `PatternPipelineProduct` descriptions

    Controls the handling of patterns data in the "src/patterns/data" directory
    """
    
    products : Optional[List[PatternPipelineProduct]] = None
    """all pipeline products"""
    
    matches: Optional[List[PatternPipelineProduct]] = None
    """pipelines specifically configured for matching, NOT generating."""
    
    directory : Directory = "../patterns/"
    """directory where pattern source lives, also where TSV exported to"""

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(PatternPipelineProduct(id=id))

@dataclass_json
@dataclass
class SSSOMMappingSetGroup(JsonSchemaMixin):
    """
    A configuration section that consists of a list of `SSSOMMappingSetProduct` descriptions
    """
    
    directory : Directory = "../mappings"

    release_mappings : bool = False
    """If set to True, mappings are copied to the release directory."""

    mapping_extractor : str = "sssom-py"
    """The tool to use to extract mappings from an ontology ('sssom-py' or 'sssom-java')."""
    
    products : Optional[List[SSSOMMappingSetProduct]] = None

    def fill_missing(self, project):
        if self.products is None:   # Huh? Ignore.
            return
        if self.release_mappings:   # All sets are released
            released_products = [p for p in self.products]
        else:   # Only some selected sets are released
            released_products = [p for p in self.products if p.release_mappings]
        if len(released_products) > 0:
            self.released_products = released_products

        for product in self.products:
            if product.maintenance == "merged":
                if product.source_mappings is None:
                    # Merge all other non-merge sets to make this one
                    product.source_mappings = [p.id for p in self.products if p.maintenance != "merged"]
                else:
                    # Check that all listed source sets exist
                    for source in product.source_mappings:
                        if source not in [p.id for p in self.products]:
                            raise Exception(f"Unknown source mapping set '{source}'")
            elif product.maintenance == "extract":
                if product.source_file is None:
                    product.source_file = "$(EDIT_PREPROCESSED)"

@dataclass_json
@dataclass
class BabelonTranslationSetGroup(JsonSchemaMixin):
    """
    A configuration section that consists of a list of `BabelonTranslationProduct` descriptions
    """
    
    directory : Directory = "../translations"

    release_merged_translations : bool = False
    """If true, a big table and JSON file is created which contains all translations."""
    
    predicates : Optional[List[str]] = field(default_factory=lambda: ['IAO:0000115', 'rdfs:label'])
    """The list of predicates that are considered during translation preparation."""
    
    oak_adapter: str = "pronto:$(ONT).obo"
    """The oak adapter that should be used to process the translation tables. Should match the 'translate_ontology' field."""
        
    translate_ontology : str = "$(ONT).obo"
    """The name of the ontology that should be translated. Should match the 'oak_adapter' field."""
    
    products : Optional[List[BabelonTranslationProduct]] = None


@dataclass_json
@dataclass
class ExportGroup(ProductGroup):
    """
    A configuration section that consists of a list of `ExportProduct` descriptions

    Controls generation of exports (typically SPARQL via robot query) into the "reports/" directory
    """
    
    products : Optional[List[ExportProduct]] = None
    """all export products"""

    directory : Directory = "reports/"
    """directory where exports are placed"""


@dataclass_json
@dataclass
class RobotPlugin(JsonSchemaMixin):
    """
    A configuration for a single ROBOT plugin
    """

    name : str = ""
    """Basename for the plugin"""

    mirror_from : Optional[str] = None
    """Automatically download the plugin from this URL"""


@dataclass_json
@dataclass
class PluginsGroup(JsonSchemaMixin):
    """
    A configuration section to list extra ROBOT plugins not provided by the ODK
    """

    plugins : Optional[List[RobotPlugin]] = None
    """The list of plugins to use"""

    
@dataclass_json
@dataclass
class OntologyProject(JsonSchemaMixin):
    """
    A configuration for an ontology project/repository

    This is divided into project-wide settings, plus
    groups of products. Products are grouped into 4
    categories (more may be added)
    """

    id : OntologyHandle = ""
    """OBO id for this ontology. Must be lowercase Examples: uberon, go, cl, envo, chebi"""

    title : str = ""
    """Concise descriptive text about this ontology"""

    git_user : str = ""
    """GIT user name (necessary for generating releases)"""

    repo : str = "noname"
    """Name of repo (do not include org). E.g. cell-ontology"""

    repo_url : str = ""
    """URL of the online repository. If set, this must point to a browsable version of the repository root."""

    github_org : str = ""
    """Name of github org or username where repo will live. Examples: obophenotype, cmungall"""

    git_main_branch : str = "main"
    """The main branch for your repo, such as main, or (now discouraged) master."""

    edit_format : str = "owl"
    """Format in which the edit file is managed, either obo or owl"""

    run_as_root: bool = False
    """if true, all commands will be executed into the container under the identity of the super-user. Use this if you have custom workflows that require admin rights (e.g. to install Debian packages not provided in the ODK)."""
    
    robot_version: Optional[str] = None
    """Only set this if you want to pin to a specific robot version"""
    
    robot_settings: Optional[CommandSettings] = None
    """Settings to pass to ROBOT such as amount of memory to be used"""
    
    robot_java_args: Optional[str] = ""
    """Java args to pass to ROBOT at runtime, such as -Xmx6G"""
    
    owltools_memory: Optional[str] = ""
    """OWLTools memory, for example 4GB."""

    use_external_date: bool = False
    """Flag to set if you want odk to use the host `date` rather than the docker internal `date`"""
    
    remove_owl_nothing: bool = False
    """Flag to set if you want odk to remove owl:Nothing from releases."""
    
    export_project_yaml: bool = False
    """Flag to set if you want a full project.yaml to be exported, including all the default options."""
    
    reasoner : str = "ELK"
    """Name of reasoner to use in ontology pipeline, see robot reason docs for allowed values"""
    
    exclude_tautologies : str = "structural"
    """Remove tautologies such as A SubClassOf: owl:Thing or owl:Nothing SubclassOf: A. For more information see http://robot.obolibrary.org/reason#excluding-tautologies"""
    
    primary_release : str = "full"
    """Which release file should be published as the primary release artefact, i.e. foo.owl"""
    
    license : str = "https://creativecommons.org/licenses/unspecified"
    """Which license is ontology supplied under - must be an IRI."""
    
    description : str = "None"
    """Provide a short description of the ontology"""
    
    use_dosdps : bool = False
    """if true use dead simple owl design patterns"""
    
    use_templates : bool = False
    """if true use ROBOT templates."""
    
    use_mappings : bool = False
    """if true use SSSOM mapping files."""
    
    use_translations : bool = False
    """if true enable babelon multilingual support."""

    use_env_file_docker : bool = False
    """if true environment variables are collected by the docker wrapper and passed into the container."""

    use_custom_import_module : bool = False
    """if true add a custom import module which is managed through a robot template. This can also be used to manage your module seed."""

    preserve_non_odk_managed_imports : bool = False
    """if true, import declarations that were added independently of the ODK will be preserved when updating the repository."""
    
    custom_makefile_header : str = """
# ----------------------------------------
# More information: https://github.com/INCATools/ontology-development-kit/
"""
    """A multiline string that is added to the Makefile"""

    use_context: bool = False
    """If True, a context file is created that allows the user to specify prefixes used across the project."""
    
    public_release : str = "none"
    """if true add functions to run automated releases (experimental). Current options are: github_curl, github_python."""

    public_release_assets : Optional[List[str]] = None
    """A list of files that gets added to a github/gitlab/etc release (as assets). If this option is not set (None), the standard ODK assets will be deployed."""
    
    release_date : bool = False
    """if true, releases will be tagged with a release date (oboInOwl:date)"""
    
    allow_equivalents : str = "asserted-only"
    """can be all, none or asserted-only (see ROBOT documentation: http://robot.obolibrary.org/reason)"""
    
    ci : Optional[List[str]] = field(default_factory=lambda: ['github_actions'])
    """continuous integration defaults; currently available: travis, github_actions, gitlab-ci"""
    
    workflows : Optional[List[str]] = field(default_factory=lambda: ['docs', 'qc'])
    """Workflows that are synced when updating the repo. Currently available: docs, diff, qc, release-diff."""
    
    import_pattern_ontology : bool = False
    """if true import pattern.owl"""

    import_component_format : str = "ofn"
    """The default serialisation for all components and imports."""
    
    create_obo_metadata : bool = True
    """if true OBO Markdown and PURL configs are created."""
    
    gzip_main : bool = False
    """if true add a gzipped version of the main artefact"""
    
    release_artefacts : List[str] = field(default_factory=lambda: ['full', 'base'])
    """A list of release artefacts you wish to be exported. Supported: base, full, baselite, simple, non-classified, 
    simple-non-classified, basic."""
    
    release_use_reasoner : bool = True
    """If set to True, the reasoner will be used during the release process. The reasoner is used for three operations:
    reason (the classification/subclassOf hierarchy computation); materialize (the materialisation of simple existential/
    object property restrictions); reduce (the removal of redundant subclassOf axioms)."""
    
    release_annotate_inferred_axioms : bool = False
    """If set to True, axioms that are inferred during the reasoning process are annotated accordingly, 
    see https://robot.obolibrary.org/reason."""

    release_materialize_object_properties : List[str] = None
    """Define which object properties to materialise at release time."""
    
    export_formats : List[str] = field(default_factory=lambda: ['owl', 'obo'])
    """A list of export formats you wish your release artefacts to be exported to, such as owl, obo, gz, ttl, db."""
    
    namespaces : Optional[List[str]] = None
    """A list of namespaces that are considered at home in this ontology. Used for certain filter commands."""
    
    use_edit_file_imports : bool = True
    """If True, ODK will release the ontology with imports explicitly specified by owl:imports in the edit file.
    If False, ODK will build and release the ontology with _all_ imports and _all_ components specified in the ODK config file."""
    
    dosdp_tools_options: str = "--obo-prefixes=true"
    """default parameters for dosdp-tools"""
    
    travis_emails : Optional[List[Email]] = None ## ['obo-ci-reports-all@groups.io']
    """Emails to use in travis configurations. """
    
    obo_format_options : str = ""
    """Additional args to pass to robot when saving to obo. TODO consider changing to a boolean for checks"""

    catalog_file : str = "catalog-v001.xml"
    """Name of the catalog file to be used by the build."""

    uribase : str = "http://purl.obolibrary.org/obo"
    """Base URI for PURLs. For an example see https://gitlab.c-path.org/c-pathontology/critical-path-ontology."""
    
    uribase_suffix : str = None
    """Suffix for the uri base. If not set, the suffix will be the ontology id by default."""
    
    contact : Optional[Person] = None
    """Single contact for ontology as required by OBO"""
    
    creators : Optional[List[Person]] = None
    """List of ontology creators (currently setting this has no effect)"""
    
    contributors : Optional[List[Person]] = None
    """List of ontology contributors (currently setting this has no effect)"""

    robot_report : Dict[str, Any] = field(default_factory=lambda: ReportConfig().to_dict())
    """Block that includes settings for ROBOT report, ROBOT verify and additional reports that are generated"""

    ensure_valid_rdfxml : bool = True
    """When enabled, ensure that any RDF/XML product file is valid"""

    extra_rdfxml_checks : bool = False
    """When enabled, RDF/XML product files are checked against additional parsers"""

    robot_plugins : Optional[PluginsGroup] = None
    """Block that includes information on the extra ROBOT plugins used by this project"""

    # product groups
    import_group : Optional[ImportGroup] = None
    """Block that includes information on all ontology imports to be generated"""

    components : Optional[ComponentGroup] = None
    """Block that includes information on all ontology components to be generated"""
    
    documentation : Optional[DocumentationGroup] = None
    """Block that includes information on all ontology components to be generated"""

    subset_group : Optional[SubsetGroup] = None
    """Block that includes information on all subsets (aka slims) to be generated"""
    
    pattern_pipelines_group : Optional[PatternPipelineGroup] = None
    """Block that includes information on all DOSDP templates used"""
    
    sssom_mappingset_group : Optional[SSSOMMappingSetGroup] = None
    """Block that includes information on all SSSOM mapping tables used"""
    
    babelon_translation_group : Optional[BabelonTranslationSetGroup] = None
    """Block that includes information on all babelon tables used"""

    release_diff : bool = False
    """When enabled, a diff is generated between the current release and the new one"""

    def fill_missing(self):
        """
        Each group consists of a list of product objects.
        The config can be lazy and just specify an id list.
        These are used to create stub product objects.

        (this adds complexity and may be removed)
        """
        if self.import_group is not None:
            self.import_group.fill_missing(self)
        if self.subset_group is not None:
            self.subset_group.fill_missing(self)
        if self.pattern_pipelines_group is not None:
            self.pattern_pipelines_group.fill_missing(self)
        if self.sssom_mappingset_group is not None:
            self.sssom_mappingset_group.fill_missing(self)
        if self.components is not None:
            self.components.fill_missing(self)

@dataclass
class ExecutionContext(JsonSchemaMixin):
    """
    Top level object that is passed to Jinja2 templates
    """
    project : Optional[OntologyProject] = None
    meta : str = ""


@dataclass
class Generator(object):
    """
    Utility class for generating a variety of ontology project artefacts
    from jinja2 templates
    """

    ## TODO: consider merging Generator and ExecutionContext?
    context : ExecutionContext = field(default_factory=ExecutionContext)

    def generate(self, input : str) -> str:
        """
        Given a path to an input template, renders the template
        using the current execution context
        """
        with open(input) as file_:
            template = Template(file_.read())
            if "ODK_VERSION" in os.environ:
                return template.render( project = self.context.project, env = {"ODK_VERSION": os.getenv("ODK_VERSION")})
            else:
                return template.render( project = self.context.project)

    def load_config(self,
                    config_file : Optional[str] = None,
                    imports : Optional[List[str]] = None,
                    title : Optional[str] = None,
                    org : Optional[str] = None,
                    repo : Optional[str] = None):
        """
        Parses a project.yaml file and uses the contents to
        set the current execution context.

        Optionally injects additional values
        """
        config_hash = None
        if config_file is None:
            project = OntologyProject()
        else:
            with open(config_file, 'r') as stream:
                h = sha256()
                h.update(stream.read().encode())
                config_hash = h.hexdigest()
                stream.seek(0)
                obj = yaml.load(stream, Loader=yaml.FullLoader)
            project = from_dict(data_class=OntologyProject, data=obj)
        if config_hash:
            project.config_hash = config_hash
        if title:
            project.title = title
        if org:
            project.github_org = org
        if repo:
            project.repo = repo
        if imports:
            if project.import_group is None:
                project.import_group = ImportGroup()
            project.import_group.ids = imports
        project.fill_missing()
        self.context = ExecutionContext(project=project)

def save_project_yaml(project : OntologyProject, path : str):
    """
    Saves an ontology project to a file in YAML format
    """
    # This is a slightly ridiculous bit of tomfoolery, but necessary
    # As PyYAML will attempt to save as a python object using !!,
    # so we must first serialize as JSON then parse than JSON to get
    # a class-free python dict tha can be safely saved
    json_str = project.to_json()
    json_obj = json.loads(json_str)
    with open(path, "w") as f:
        f.write(yaml.dump(json_obj, default_flow_style=False))
        
def unpack_files(basedir, txt, policies=[]):
    """
    This unpacks a custom tar-like format in which multiple file paths
    can be specified, separated by ^^^s

    See the file template/_dynamic_files.jinja2 for an example of this
    """
    MARKER = '^^^ '
    lines = txt.split("\n")
    f = None
    tgts = []
    ignore = False
    for line in lines:
        if line.startswith(MARKER):
            # Close previous file, if any
            if f != None:
                f.close()
            filename = line.replace(MARKER, "")
            path = os.path.join(basedir, filename)
            ignore = not must_install_file(filename, path, policies)
            if not ignore:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                f = open(path,"w")
                tgts.append(path)
                logging.info('  Unpacking into: {}'.format(path))
        elif not ignore:
            if f is None:
                if line == "":
                    continue
                else:
                    raise Exception('File marker "{}" required in "{}"'.format(MARKER, line))
            f.write(line + "\n")
    if f != None:
        f.close()
    return tgts

def get_template_name(templatedir, pathname):
    """
    Helper function to get the user-visible name of a template file
    from its complete pathname in the template directory.

    For example, if the pathname is
    "/tools/template/src/ontology/run.sh.jinja2", this will return
    "src/ontology/run.sh".
    """
    name = pathname.replace(templatedir, "")
    if len(name) > 0 and name[0] == '/':
        name = name[1:]
    if name.endswith(TEMPLATE_SUFFIX):
        name = name.replace(TEMPLATE_SUFFIX, "")
    return name

# Available policies for installing a file
IF_MISSING, ALWAYS, NEVER = range(3)

def must_install_file(templatefile, targetfile, policies):
    """
    Given a template filename, indicate whether the file should be
    installed according to any per-file policy.

    policies is a list of (PATTERN,POLICY) tuples where PATTERN is
    a shell-like globbing pattern and POLICY is the update policy
    that should be applied to any template whose pathname matches
    the pattern.

    Patterns are tested in the order they are found in the list,
    and the first match takes precedence over any subsequent match.
    If there is no match, the default policy is IF_MISSING.

    Valid policies are:
    * IF_MISSING: install the file if it does not already exist
    * ALWAYS: always install the file, overwrite any existing file
    * NEVER: never install the file
    """
    policy = IF_MISSING
    for pattern, pattern_policy in policies:
        if fnmatch.fnmatch(templatefile, pattern):
            policy = pattern_policy
            break
    if policy == ALWAYS:
        return True
    elif policy == NEVER:
        return False
    else:
        return not os.path.exists(targetfile)

def install_template_files(generator, templatedir, targetdir, policies=[]):
    """
    Installs all template-derived files into a target directory.
    """
    tgts = []
    for root, subdirs, files in os.walk(templatedir):
        tdir = root.replace(templatedir,targetdir+"/")
        os.makedirs(tdir, exist_ok=True)

        # first copy plain files...
        for f in [f for f in files if not f.endswith(TEMPLATE_SUFFIX)]:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            if must_install_file(get_template_name(templatedir, srcf), tgtf, policies):
                logging.info('  Copying: {} -> {}'.format(srcf, tgtf))
                # copy file directly, no template expansions
                copy(srcf, tgtf)
                tgts.append(tgtf)
        logging.info('Applying templates')
        # ...then apply templates
        for f in [f for f in files if f.endswith(TEMPLATE_SUFFIX)]:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            derived_file = tgtf.replace(TEMPLATE_SUFFIX, "")
            if f.startswith("_dynamic"):
                logging.info('  Unpacking: {}'.format(derived_file))
                tgts += unpack_files(tdir, generator.generate(srcf), policies)
            elif must_install_file(get_template_name(templatedir, srcf), derived_file, policies):
                logging.info('  Compiling: {} -> {}'.format(srcf, derived_file))
                with open(derived_file,"w") as s:
                    s.write(generator.generate(srcf))
                tgts.append(derived_file)
                copymode(srcf, derived_file)
    return tgts

def update_gitignore(generator, template_file, target_file):
    """
    Update a potentially existing .gitignore file while preserving
    its non-ODK-managed contents.
    """
    if not os.path.exists(template_file):
        # Should not happen as we should always have a .gitignore
        # template, but just in case
        return

    existing_lines = []
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            exclude = False
            for line in [l.strip() for l in f]:
                if line == "# ODK-managed rules, do not modify":
                    exclude = True
                elif line == "# End of ODK-managed rules":
                    exclude = False
                elif not exclude:
                    existing_lines.append(line)

    already_written = {}
    with open(target_file, "w") as f:
        for line in generator.generate(template_file).split("\n"):
            if len(line) > 0:
                already_written[line] = 1
            f.write(line + "\n")
        for line in [l for l in existing_lines if l not in already_written]:
            f.write(line + "\n")

def update_xml_catalog(generator, template_file, target_file):
    """
    Updates a potentially existing XML catalog file while preserving
    its non-ODK-managed contents.
    """
    if not os.path.exists(template_file):
        return

    CATALOG_NS = 'urn:oasis:names:tc:entity:xmlns:xml:catalog'
    XML_NS = 'http://www.w3.org/XML/1998/namespace'
    CATALOG_GROUP = '{' + CATALOG_NS + '}group'
    CATALOG_URI = '{' + CATALOG_NS + '}uri'
    XML_BASE = '{' + XML_NS + '}base'

    template_entries = {}
    ElementTree.register_namespace('', CATALOG_NS)

    def process_children(node):
        to_remove = []
        for child in node:
            if child.tag == CATALOG_URI:
                # Remove the entry if it corresponds to one already set
                # by the ODK-managed group.
                name = child.attrib.get('name')
                uri = child.attrib.get('uri')
                if name and uri and name + '@' + uri in template_entries:
                    to_remove.append(child)
            elif child.tag == CATALOG_GROUP:
                if child.attrib.get('id') == 'odk-managed-catalog':
                    # Completely exclude that group, so that it is
                    # entirely replaced by the one from the template.
                    to_remove.append(child)
                else:
                    # Some existing catalog groups have an empty
                    # xml:base="" attribute; such an attribute is
                    # incorrect according to the XML spec.
                    if child.attrib.get(XML_BASE) == '':
                        child.attrib.pop(XML_BASE)
                    process_children(child)
        for child in to_remove:
            node.remove(child)

    template_root = DefusedElementTree.fromstring(generator.generate(template_file))
    if os.path.exists(target_file):
        # Make a list of the entries in the managed catalog
        odk_managed_group = template_root.find(CATALOG_GROUP)
        for managed_uri in odk_managed_group.findall(CATALOG_URI):
            template_entries[managed_uri.attrib['name'] + '@' + managed_uri.attrib['uri']] = 1

        # Add the contents of the existing catalog
        existing_tree = DefusedElementTree.parse(target_file)
        process_children(existing_tree.getroot())
        for child in existing_tree.getroot():
            template_root.append(child)

    new_catalog = ElementTree.ElementTree(template_root)
    ElementTree.indent(new_catalog, space='  ', level=0)
    new_catalog.write(target_file, encoding='UTF-8', xml_declaration=True)

def update_import_declarations(project, pluginsdir='/tools/robot-plugins'):
    """
    Updates the project's -edit file to ensure it contains import
    declarations for all the import modules, components, and
    pattern-derived files declared in the ODK configuration.
    """
    base = project.uribase + '/'
    if project.uribase_suffix is not None:
        base += project.uribase_suffix
    else:
        base += project.id

    if not 'ROBOT_PLUGINS_DIRECTORY' in os.environ:
        os.environ['ROBOT_PLUGINS_DIRECTORY'] = pluginsdir

    ignore_missing_imports = '-Dorg.semantic.web.owlapi.model.parameters.ConfigurationOptions.MISSING_IMPORT_HANDLING_STRATEGY=SILENT'
    if 'ROBOT_JAVA_ARGS' in os.environ:
        os.environ['ROBOT_JAVA_ARGS'] += ' ' + ignore_missing_imports
    else:
        os.environ['ROBOT_JAVA_ARGS'] = ignore_missing_imports

    cmd = f'robot odk:import -i {project.id}-edit.{project.edit_format}'
    if not project.preserve_non_odk_managed_imports:
        cmd += ' --exclusive true'

    if project.import_group.use_base_merging:
        cmd += f' --add {base}/imports/merged_import.owl'
    else:
        for product in project.import_group.products:
            cmd += f' --add {base}/imports/{product.id}_import.owl'
    for component in project.components.products:
        cmd += f' --add {base}/components/{component.filename}'
    if project.use_dosdps:
        cmd += f' --add {base}/patterns/definitions.owl'
        if project.import_pattern_ontology:
            cmd += f' --add {base}/patterns/pattern.owl'

    if project.edit_format == 'owl':
        cmd += f' convert -f ofn -o {project.id}-edit.owl'
    else:
        cmd += f' convert --check false -o {project.id}-edit.obo'
    runcmd(cmd)

def format_yaml_error(file, exc):
    """
    Prints a human-readable error message from a YAML parser error.
    """
    msg = "Cannot parse configuration file"
    if hasattr(exc, 'problem_mark'):
        err_line = exc.problem_mark.line
        err_column = exc.problem_mark.column
        msg += f"\nLine {err_line + 1}, column {err_column + 1}: {exc.problem}"
        with open(file, 'r') as f:
            line = f.readline()
            linenr = 1
            while line and linenr <= err_line:
                linenr += 1
                line = f.readline()
        msg += "\n" + line.rstrip()
        msg += "\n" + ' ' * err_column + '^'
    else:
        msg += ": unknown YAML error"
    return msg


## ========================================
## Command Line Wrapper
## ========================================
## this could potentially be moved to a separate file
## somewhat convenient to lump for now

import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-C', '--config', type=click.Path(exists=True))
@click.option('-T', '--templatedir',  default='/tools/templates/')
@click.option('-i', '--input',  type=click.Path(exists=True))
@click.option('-o', '--output')
def create_makefile(config, templatedir, input, output):
    """
    For testing purposes
    """
    mg = Generator()
    try:
        mg.load_config(config)
    except yaml.YAMLError as exc:
        raise click.ClickException(format_yaml_error(config, exc))
    print(mg.generate('{}/src/ontology/Makefile.jinja2'.format(templatedir)))

@cli.command()
@click.option('-C', '--config', type=click.Path(exists=True))
@click.option('-T', '--templatedir',  default='/tools/templates/')
@click.option('-i', '--input',  type=click.Path(exists=True))
@click.option('-o', '--output')
def create_dynfile(config, templatedir, input, output):
    """
    For testing purposes
    """
    mg = Generator()
    try:
        mg.load_config(config)
    except yaml.YAMLError as exc:
        raise click.ClickException(format_yaml_error(config, exc))
    print(mg.generate('{}/_dynamic_files.jinja2'.format(templatedir)))
    
@cli.command()
@click.option('-C', '--config', type=click.Path(exists=True))
@click.option('-o', '--output', required=True)
def export_project(config, output):
    """
    For testing purposes
    """
    mg = Generator()
    try:
        mg.load_config(config)
    except yaml.YAMLError as exc:
        raise click.ClickException(format_yaml_error(config, exc))
    project = mg.context.project
    save_project_yaml(project, output)
    
@cli.command()
@click.option('-c', '--class_name', type=str, default="OntologyProject")
def dump_schema(class_name):
    """
    Dumps the python schema as json schema.

    Note: this is intended primarily at odk developers
    """
    import json
    if class_name=="all":
        # This allows us to dump all schemas at once, but the result is not legal JSON and only
        # useful for generating docs
        classes = ['OntologyProject', 'ImportProduct', 'PatternPipelineGroup']
        #classes = ['OntologyProject', 'ImportGroup', 'ImportProduct', 'SubsetGroup', 
        #           'SubsetProduct', 'ReportConfig', 'ExportGroup', 'ExportProduct', 
        #           'ProductGroup', 'Product', 'ComponentGroup', 'ComponentProduct', 
        #           'PatternPipelineGroup', 'PatternPipelineProduct', 'SSSOMMappingSetGroup', 'SSSOMMappingSetProduct']
        for k in classes:
            print(json.dumps(globals()[k].json_schema(), sort_keys=True, indent=4))
    else:
        clazz = globals()[class_name]  # Get the class object from the globals dictionary
        print(json.dumps(clazz.json_schema(), sort_keys=True, indent=4))

@cli.command()
@click.option('-T', '--templatedir', default='/tools/templates/')
def update(templatedir):
    """
    Updates a pre-existing repository. This command is expected to be
    run from within the src/ontology directory (the directory
    containing the configuration file).
    """
    config_matches = list(glob.glob('*-odk.yaml'))
    if len(config_matches) == 0:
        raise click.ClickException("No ODK configuration file found")
    elif len(config_matches) > 1:
        raise click.ClickException("More than ODK configuration file found")
    config = config_matches[0]
    mg = Generator()
    try:
        mg.load_config(config)
    except yaml.YAMLError as exc:
        raise click.ClickException(format_yaml_error(config, exc))
    project = mg.context.project

    # When updating, for most files, we only install them if
    # they do not already exist in the repository (typically
    # because they are new files that didn't exist in the
    # templates of the previous version of the ODK). But a
    # handful of files are not reinstalled even if they are
    # missing (e.g. DOSDP example files) or on the contrary
    # always reinstalled to overwrite any local changes (e.g.
    # the main Makefile). We declare the corresponding policies.
    policies = [
            ('CODE_OF_CONDUCT.md', NEVER),
            ('CONTRIBUTING.md', NEVER),
            ('issue_template.md', NEVER),
            ('README.md', NEVER),
            ('src/patterns/data/default/example.tsv', NEVER),
            ('src/patterns/dosdp-patterns/example.yaml', NEVER),
            ('src/ontology/Makefile', ALWAYS),
            ('src/ontology/run.sh', ALWAYS),
            ('src/ontology/catalog-v001.xml', NEVER),
            ('src/sparql/*', ALWAYS),
            ('docs/odk-workflows/*', ALWAYS),
            ('.gitignore', NEVER)
            ]
    if 'github_actions' in project.ci:
        for workflow in ['qc', 'diff', 'release-diff']:
            if workflow in project.workflows:
                policies.append(('.github/workflows/' + workflow + '.yml', ALWAYS))
        if project.documentation is not None and 'docs' in project.workflows:
            policies.append(('.github/workflows/docs.yml', ALWAYS))
    if not project.robot_report.get('custom_profile', False):
        policies.append(('src/ontology/profile.txt', NEVER))

    # Proceed with template instantiation, using the policies
    # declared above. We instantiate directly at the root of
    # the repository -- no need for a staging directory.
    install_template_files(mg, templatedir, '../..', policies)

    # Special procedures to update some ODK-managed files that
    # may have been manually edited.
    update_gitignore(mg, templatedir + '/.gitignore.jinja2', '../../.gitignore')
    update_xml_catalog(mg, templatedir + '/src/ontology/catalog-v001.xml.jinja2', 'catalog-v001.xml')

    update_import_declarations(project)

    print("WARNING: This file should be manually migrated: mkdocs.yaml")
    if 'github_actions' in project.ci and 'qc' not in project.workflows:
        print("WARNING: Your QC workflows have not been updated automatically.")
        print("         Please update the ODK version number in .github/workflows/qc.yml")
    print("Ontology repository update successfully completed.")

@cli.command()
@click.option('-C', '--config',       type=click.Path(exists=True),
              help="""
              path to a YAML configuration.
              See examples folder for examples.
              This is optional, configuration can also be passed
              by command line, but an explicit config file is preferred.
              """)

@click.option('-c', '--clean/--no-clean', default=False)
@click.option('-T', '--templatedir',  default='/tools/templates/')
@click.option('-D', '--outdir',       default=None)
@click.option('-d', '--dependencies', multiple=True)
@click.option('-t', '--title',        type=str)
@click.option('-u', '--user',         type=str)
@click.option('-s', '--source',       type=str,
              help="""
              path to existing source for ontology edit file. 
              Optional. If not passed, a stub ontology will be created.
              """)
@click.option('-v', '--verbose',      count=True)
@click.option('-g', '--skipgit',      default=False, is_flag=True)
@click.option('-n', '--gitname',      default=None)
@click.option('-e', '--gitemail',     default=None)
@click.option('-r', '--commit-artefacts', default=False, is_flag=True)
@click.argument('repo', nargs=-1)
def seed(config, clean, outdir, templatedir, dependencies, title, user, source, verbose, repo, skipgit, gitname, gitemail, commit_artefacts):
    """
    Seeds an ontology project
    """
    tgts = []
    mg = Generator()
    if len(repo) > 0:
        if len(repo) > 1:
            raise click.ClickException('max one repo; current={}'.format(repo))
        repo = repo[0]
    try:
        mg.load_config(config,
                       imports=dependencies,
                       title=title,
                       org=user,
                       repo=repo)
    except yaml.YAMLError as exc:
        raise click.ClickException(format_yaml_error(config, exc))
    project = mg.context.project
    if project.id is None or project.id == "":
        project.id = repo
    if outdir is None:
        outdir = "target/{}".format(project.id)
    if not skipgit:
        if not "GIT_AUTHOR_NAME" in os.environ and not gitname:
            raise click.ClickException("missing Git username; set GIT_AUTHOR_NAME or use --gitname")
        if not "GIT_AUTHOR_EMAIL" in os.environ and not gitemail:
            raise click.ClickException("missing Git email; set GIT_AUTHOR_EMAIL or use --gitemail")
    if clean:
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    if not os.path.exists(templatedir) and templatedir == "/tools/templates/":
        logging.info("No templates folder in /tools/; assume not in docker context")
        templatedir = "./template"
    policies = []
    if not project.robot_report.get('custom_profile', False):
        policies.append(('src/ontology/profile.txt', NEVER))
    tgts += install_template_files(mg, templatedir, outdir, policies)

    tgt_project_file = "{}/project.yaml".format(outdir)
    if project.export_project_yaml:
        save_project_yaml(project, tgt_project_file)
        tgts.append(tgt_project_file)
    if source is not None:
        copy(source, "{}/src/ontology/{}-edit.{}".format(outdir, project.id, project.edit_format))
    odk_config_file = "{}/src/ontology/{}-odk.yaml".format(outdir, project.id)
    tgts.append(odk_config_file)
    if config is not None:
        copy(config, odk_config_file)
    else:
        save_project_yaml(project, odk_config_file)
    logging.info("Created files:")
    for tgt in tgts:
        logging.info("  File: {}".format(tgt))
    if not skipgit:
        if gitname is not None:
            os.environ['GIT_AUTHOR_NAME'] = gitname
            os.environ['GIT_COMMITTER_NAME'] = gitname
        if gitemail is not None:
            os.environ['GIT_AUTHOR_EMAIL'] = gitemail
            os.environ['GIT_COMMITTER_EMAIL'] = gitemail
        runcmd("cd {dir} && git init -b {branch} && git add {files} && git commit -m 'initial commit'".
               format(dir=outdir,
                      branch=project.git_main_branch,
                      files=" ".join([t.replace(outdir, ".", 1) for t in tgts])))
        runcmd("cd {dir}/src/ontology && make all_assets && cp $(make show_release_assets) ../../"
               .format(dir=outdir))
        if commit_artefacts:
            runcmd("cd {dir}/src/ontology "
                    "&& for asset in $(make show_release_assets) ; do git add -f ../../$asset ; done"
                   .format(dir=outdir))
        runcmd("cd {dir} && if [ -n \"$(git status -s)\" ]; then git commit -a -m 'initial build' ; fi"
               .format(dir=outdir))
        print("\n\n####\nNEXT STEPS:")
        print(" 0. Examine {} and check it meets your expectations. If not blow it away and start again".format(outdir))
        print(" 1. Go to: https://github.com/new")
        print(" 2. The owner MUST be {org}. The Repository name MUST be {repo}".format(org=project.github_org, repo=project.repo))
        print(" 3. Do not initialize with a README (you already have one)")
        print(" 4. Click Create")
        print(" 5. See the section under '…or push an existing repository from the command line'")
        print("    E.g.:")
        print("cd {}".format(outdir))
        print("git remote add origin git@github.com:{org}/{repo}.git".format(org=project.github_org, repo=project.repo))
        print("git push -u origin {branch}\n".format(branch=project.git_main_branch))
        print("BE BOLD: you can always delete your repo and start again\n")
        print("")
        print("FINAL STEPS:")
        print("Follow your customized instructions here:\n")
        print("    https://github.com/{org}/{repo}/blob/main/src/ontology/README-editors.md".format(org=project.github_org, repo=project.repo))
    else:
        print("Repository files have been successfully copied, but no git commands have been run.")


def runcmd(cmd):
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, err) = p.communicate()
    logging.info('OUT: {}'.format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))
    

            
                
if __name__ == "__main__":
    cli()
