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
from shutil import copyfile
import logging

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
class ComponentProduct():
    """
    Represents an individual component
    Examples: a file external to the edit file that contains axioms that belong to this ontology
    Components are usually maintained manually.
    """
    
    filename: Optional[str] = None
    """The filename of this component"""

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

@dataclass_json
@dataclass
class PatternPipelineProduct(Product):
    """
    Represents an individual pattern pipeline
    Examples: manual curation pipeline, auto curation pipeline
    Each pipeline gets their own specific directory
    """
    dosdp_tools_options: str = "--obo-prefixes=true"

@dataclass_json
@dataclass
class PatternProduct(Product):
    """Represents a DOSDP template product
    
    The products here can be manfested as CSVs (from 'parse'ing OWL)
    or they may be OWL (from the dosdp 'generate' command)
    """
    pass


@dataclass_json
@dataclass
class RoboTemplateProduct(Product):
    """
    Represents a ROBOT template
    """
    pass

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

    directory : Directory = "imports/"
    """directory where imports are extracted into to"""

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(ImportProduct(id=id))

@dataclass_json
@dataclass
class ComponentGroup(ComponentProduct):
    """
    A configuration section that consists of a list of `ComponentProduct` descriptions

    Controls extraction of import modules via robot extract into the "components/" directory
    """
    
    products : Optional[List[ComponentProduct]] = None
    """all component products"""

    directory : Directory = "components/"
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

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(PatternPipelineProduct(id=id))
            
@dataclass_json
@dataclass
class PatternGroup(ProductGroup):
    """
    A configuration section that consists of a list of `PatternProduct` descriptions

    """
    
    products : Optional[List[PatternProduct]] = None
    """all DOSDP pattern products"""

    directory : Directory = "../patterns/"
    """directory where pattern source lives, also where TSV exported to"""

    
@dataclass_json
@dataclass
class RoboTemplateGroup():
    """
    A configuration section that consists of a list of `RoboTemplateProduct` descriptions
    """
    
    directory : Directory = "../templates/"
    
    products : Optional[List[RoboTemplateProduct]] = None

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

    repo : str = ""
    """Name of repo (do not include org). E.g. cell-ontology"""
    
    github_org : str = ""
    """Name of github org or username where repo will live. Examples: obophenotype, cmungall"""

    edit_format : str = 'owl'
    """Format in which the edit file is managed, either obo or owl"""
    
    robot_version: Optional[str] = None
    """Only set this if you want to pin to a specific robot version"""
    
    robot_settings: Optional[CommandSettings] = None
    """Settings to pass to ROBOT such as amount of memory to be used"""
    
    robot_java_args: Optional[str] = ""
    """Java args to pass to ROBOT at runtime, such as -Xmx6G"""

    use_external_date: bool = False
    """Flag to set if you want odk to use the host `date` rather than the docker internal `date`"""
    
    reasoner : str = 'ELK'
    """Name of reasoner to use in ontology pipeline, see robot reason docs for allowed values"""
    
    primary_release : str = 'full'
    """Which release file should be published as the primary release artefact, i.e. foo.owl"""
    
    license : str = 'Unspecified'
    """Which license is ontology supplied under; ideally CC-BY."""
    
    description : str = 'None'
    """Provide a short description of the ontology"""
    
    use_dosdps : bool = False
    """if true use dead simple owl design patterns"""
    
    import_pattern_ontology : bool = False
    """if true import pattern.owl"""
    
    gzip_main : bool = False
    """if true add a gzipped version of the main artefact"""
    
    release_artefacts : List[str] = field(default_factory=lambda: ['full', 'base'])
    """A list of release artefacts you wish to be exported."""
    
    export_formats : List[str] = field(default_factory=lambda: ['owl', 'obo'])
    """A list of export formats you wish your release artefacts to be exported to, such as owl, obo, gz, ttl."""
    
    namespaces : Optional[List[str]] = None
    """A list of namespaces that are considered at home in this ontology. Used for certain filter commands."""

    dosdp_tools_options: str = "--obo-prefixes=true"
    """default parameters for dosdp-tools"""
    
    report_fail_on : Optional[str] = None
    """see robot report docs for details. """
    
    travis_emails : Optional[List[Email]] = None ## ['obo-ci-reports-all@groups.io']
    """Emails to use in travis configurations. """
    
    obo_format_options : str = ""
    """Additional args to pass to robot when saving to obo. TODO consider changing to a boolean for checks"""

    catalog_file : str = "catalog-v001.xml"
    """Name of the catalog file to be used by the build."""

    uribase : str = 'http://purl.obolibrary.org/obo'
    """Base URI for PURLs. DO NOT MODIFY AT THIS TIME, code is still hardwired for OBO """
    
    contact : Optional[Person] = None
    """Single contact for ontology as required by OBO"""
    
    creators : Optional[List[Person]] = None
    """List of ontology creators (currently setting this has no effect)"""
    
    contributors : Optional[List[Person]] = None
    """List of ontology contributors (currently setting this has no effect)"""

    # product groups
    import_group : Optional[ImportGroup] = None
    """Block that includes information on all ontology imports to be generated"""

    components : Optional[ComponentGroup] = None
    """Block that includes information on all ontology components to be generated"""

    subset_group : Optional[SubsetGroup] = None
    """Block that includes information on all subsets (aka slims) to be generated"""

    pattern_group : Optional[PatternGroup] = None
    """Block that includes information on all DOSDP templates used"""
    
    pattern_pipelines_group : Optional[PatternPipelineGroup] = None
    """Block that includes information on all ontology imports to be generated"""

    robotemplate_group : Optional[RoboTemplateGroup] = None
    """Block that includes information on all ROBOT templates used"""

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
        if config_file is None:
            project = OntologyProject()
        else:
            obj = yaml.load(config_file)
            project = from_dict(data_class=OntologyProject, data=obj)
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
@click.option('-C', '--config', type=click.File('r'))
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
@click.option('-C', '--config', type=click.File('r'))
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
@click.option('-C', '--config', type=click.File('r'))
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
@click.option('-C', '--config',       type=click.File('r'))
@click.option('-c', '--clean/--no-clean', default=False)
@click.option('-T', '--templatedir',  default='/tools/templates/')
@click.option('-D', '--outdir',       default=None)
@click.option('-d', '--dependencies', multiple=True)
@click.option('-t', '--title',        type=str)
@click.option('-u', '--user',         type=str)
@click.option('-s', '--source',       type=str)
@click.option('-v', '--verbose',      count=True)
@click.option('-g', '--skipgit',      default=False)
@click.argument('repo', nargs=-1)
def seed(config, clean, outdir, templatedir, dependencies, title, user, source, verbose, repo, skipgit):
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
                copyfile(srcf, tgtf)
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

    tgt_project_file = "{}/project.yaml".format(outdir)
    save_project_yaml(project, tgt_project_file)
    tgts.append(tgt_project_file)
    if source is not None:
        copyfile(source, "{}/src/ontology/{}-edit.{}".format(outdir, project.id, project.edit_format))
    logging.info("Created files:")
    for tgt in tgts:
        logging.info("  File: {}".format(tgt))
    if not skipgit:
        runcmd("cd {dir} && git init && git add {files}".
               format(dir=outdir,
                      files=" ".join([t.replace(outdir, ".", 1) for t in tgts])))
        runcmd("cd {}/src/ontology && make && git commit -m 'initial commit' -a && make prepare_initial_release && git commit -m 'first release'".format(outdir))
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
        print("git push -u origin master\n")
        print("BE BOLD: you can always delete your repo and start again\n")
        print("")
        print("FINAL STEPS:")
        print("Folow your customized instructions here:\n")
        print("    https://github.com/{org}/{repo}/blob/master/src/ontology/README-editors.md".format(org=project.github_org, repo=project.repo))
    else:
        print("Repository files have been successfully copied, but no git commands have been run.")


def runcmd(cmd):
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = p.communicate()
    logging.info('OUT: {}')
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))
    

            
                
if __name__ == "__main__":
    cli()
