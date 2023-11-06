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
import subprocess
import shutil
from shutil import copy, copymode
import logging
from hashlib import sha256

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
    """If true, the component will be sourced from on or more SSSOM mapping files"""
    
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
    
    module_type_slme : str = "BOT"
    """SLME module type. Supported: BOT, TOP, STAR"""
    
    annotation_properties : List[str] = field(default_factory=lambda: ['rdfs:label', 'IAO:0000115'])
    """Define which annotation properties to pull in."""
    
    slme_individuals : str = "include"
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

    def fill_missing(self):
        if self.products is None:
            self.products = []
        if self.ids is not None:
            for id in self.ids:
                if id not in [p.id for p in self.products]:
                    self._add_stub(id)
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
    
    base_merge_drop_equivalent_class_axioms: bool = True
    """If set to true, equivalent class axioms will be removed before extracting a module with the base-merging process."""

    exclude_iri_patterns: Optional[List[str]] = None
    """List of IRI patterns. If set, IRIs matching and IRI pattern will be removed from the import."""
    
    export_obo: bool = False
    """If set to true, modules will not only be created in OWL, but also OBO format"""
    
    annotation_properties : List[str] = field(default_factory=lambda: ['rdfs:label', 'IAO:0000115'])
    """Define which annotation properties to pull in."""
    
    directory : Directory = "imports/"
    """directory where imports are extracted into to"""
    
    annotate_defined_by : bool = False
    """If set to true, the annotation rdfs:definedBy is added for each external class. 
       In the case of use_base_merging is also true, this will be added to the imports/merged_import.owl file.
       When imports are not merged, the annotation is added during the release process to the full release artefact.
    """

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(ImportProduct(id=id))

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
class ComponentGroup(ComponentProduct):
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
    
    products : Optional[List[SSSOMMappingSetProduct]] = None

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
class OntologyProject(JsonSchemaMixin):
    """
    A configuration for an ontology project/repository

    This is divided into project-wide settings, plus
    groups of products. Products are grouped into 4
    categories (more may be added)
    """

    id : OntologyHandle = ""
    """OBO id for this ontology. Must be lowecase Examples: uberon, go, cl, envo, chebi"""

    title : str = ""
    """Concise descriptive text about this ontology"""

    git_user : str = ""
    """GIT user name (necessary for generating releases)"""

    repo : str = ""
    """Name of repo (do not include org). E.g. cell-ontology"""
    
    github_org : str = ""
    """Name of github org or username where repo will live. Examples: obophenotype, cmungall"""
    
    git_main_branch : str = "main"
    """The main branch for your repo, such as main, or (now discouraged) master."""

    edit_format : str = "owl"
    """Format in which the edit file is managed, either obo or owl"""
    
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

    use_env_file_docker : bool = False
    """if true environment variables are collected by the docker wrapper and passed into the container."""

    use_custom_import_module : bool = False
    """if true add a custom import module which is managed through a robot template. This can also be used to manage your module seed."""
    
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
    
    workflows : Optional[List[str]] = field(default_factory=lambda: ['docs'])
    """Workflows that are synced when updating the repo. Currently available: docs, diff, qc."""
    
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
    reason (the classification/subclassOf hierarchy computaton); materialize (the materialisation of simple existential/
    object property restrictions); reduce (the removal of redundant subclassOf axioms)."""

    release_materialize_object_properties : List[str] = None
    """Define which object properties to materialise at release time."""
    
    export_formats : List[str] = field(default_factory=lambda: ['owl', 'obo'])
    """A list of export formats you wish your release artefacts to be exported to, such as owl, obo, gz, ttl."""
    
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

    ensure_valid_rdfxml : bool = False
    """When enabled, ensure that any RDF/XML product file is valid"""

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
            self.import_group.fill_missing()
        if self.subset_group is not None:
            self.subset_group.fill_missing()
        if self.pattern_pipelines_group is not None:
            self.pattern_pipelines_group.fill_missing()

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
    context : ExecutionContext = ExecutionContext()

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
                try:
                    obj = yaml.load(stream, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    print(exc)
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
        
def unpack_files(basedir, txt):
    """
    This unpacks a custom tar-like format in which multiple file paths
    can be specified, separated by ^^^s

    See the file template/_dynamic_files.jinja2 for an example of this
    """
    MARKER = '^^^ '
    lines = txt.split("\n")
    f = None
    tgts = []
    for line in lines:
        if line.startswith(MARKER):
            path = os.path.join(basedir, line.replace(MARKER, ""))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if f != None:
                f.close()
            f = open(path,"w")
            tgts.append(path)
            logging.info('  Unpacking into: {}'.format(path))
        else:
            if f is None:
                if line == "":
                    continue
                else:
                    raise Exception('File marker "{}" required in "{}"'.format(MARKER, line))
            f.write(line + "\n")
    if f != None:
        f.close()
    return tgts

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
    mg.load_config(config)
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
    mg.load_config(config)
    print(mg.generate('{}/_dynamic_files.jinja2'.format(templatedir)))
    
@cli.command()
@click.option('-C', '--config', type=click.Path(exists=True))
@click.option('-o', '--output', required=True)
def export_project(config, output):
    """
    For testing purposes
    """
    mg = Generator()
    mg.load_config(config)
    project = mg.context.project
    save_project_yaml(project, output)
    
@cli.command()
def dump_schema():
    """
    Dumps the python schema as json schema.

    Note: this is intended primarily at odk developers
    """
    import json
    print(json.dumps(OntologyProject.json_schema(), sort_keys=True, indent=4))
    print(json.dumps(ImportProduct.json_schema(), sort_keys=True, indent=4))
    print(json.dumps(PatternPipelineProduct.json_schema(), sort_keys=True, indent=4))


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
@click.argument('repo', nargs=-1)
def seed(config, clean, outdir, templatedir, dependencies, title, user, source, verbose, repo, skipgit, gitname, gitemail):
    """
    Seeds an ontology project
    """
    tgts = []
    mg = Generator()
    if len(repo) > 0:
        if len(repo) > 1:
            raise Exception('max one repo; current={}'.format(repo))
        repo = repo[0]
    else:
        repo = None
    mg.load_config(config,
                   imports=dependencies,
                   title=title,
                   org=user,
                   repo=repo)
    project = mg.context.project
    if project.id is None or project.id == "":
        project.id = repo
    if outdir is None:
        outdir = "target/{}".format(project.id)
    if clean:
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    if not os.path.exists(templatedir) and templatedir == "/tools/templates/":
        logging.info("No templates folder in /tools/; assume not in docker context")
        templatedir = "./template"
    for root, subdirs, files in os.walk(templatedir):
        tdir = root.replace(templatedir,outdir+"/")
        os.makedirs(tdir, exist_ok=True)

        # first copy plain files...
        for f in files:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            logging.info('  Copying: {} -> {}'.format(srcf, tgtf))
            if not tgtf.endswith(TEMPLATE_SUFFIX):
                # copy file directly, no template expansions
                copy(srcf, tgtf)
                tgts.append(tgtf)
        logging.info('Applying templates')
        # ...then apply templates
        for f in files:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            if srcf.endswith(TEMPLATE_SUFFIX):
                derived_file = tgtf.replace(TEMPLATE_SUFFIX, "")
                with open(derived_file,"w") as s:
                    if f.startswith("_dynamic"):
                        logging.info('  Unpacking: {}'.format(derived_file))
                        tgts += unpack_files(tdir, mg.generate(srcf))
                        s.close()
                        os.remove(derived_file)
                    else:
                        logging.info('  Compiling: {} -> {}'.format(srcf, derived_file))
                        s.write(mg.generate(srcf))
                        tgts.append(derived_file)
                if not f.startswith("_dynamic"):
                    copymode(srcf, derived_file)

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
        runcmd("cd {dir} && git init && git add {files}".
               format(dir=outdir,
                      files=" ".join([t.replace(outdir, ".", 1) for t in tgts])))
        runcmd("cd {dir}/src/ontology && make && git commit -m 'initial commit' -a && git branch -M {branch} && make prepare_initial_release && git commit -m 'first release'".format(dir=outdir, branch=project.git_main_branch))
        print("\n\n####\nNEXT STEPS:")
        print(" 0. Examine {} and check it meets your expectations. If not blow it away and start again".format(outdir))
        print(" 1. Go to: https://github.com/new")
        print(" 2. The owner MUST be {org}. The Repository name MUST be {repo}".format(org=project.github_org, repo=project.repo))
        print(" 3. Do not initialize with a README (you already have one)")
        print(" 4. Click Create")
        print(" 5. See the section under '…or push an existing repository from the command line'")
        print("    E.g.:")
        print("cd {}".format(outdir))
        print("git remote add origin git\@github.com:{org}/{repo}.git".format(org=project.github_org, repo=project.repo))
        print("git branch -M {branch}\n".format(branch=project.git_main_branch))
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
