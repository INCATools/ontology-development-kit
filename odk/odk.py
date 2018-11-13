"""
Generate artefacts (Makefile, default ontology edit file, imports) from a project configuration

See https://github.com/ontodev/robot/issues/37

SUBJECT TO CHANGE!

To test:

python3 odk/odk.py create_makefile -c examples/envo.yaml
"""
from typing import Optional, Set, List, Union, Dict, Any
from dataclasses import dataclass, field
from dataclasses_jsonschema import JsonSchemaMixin
from jinja2 import Template
from dacite import from_dict
import yaml
import os
from shutil import copyfile
import logging

logging.basicConfig(level=logging.INFO)
TEMPLATE_SUFFIX = '.jinja2'

# Primitive Types
OntologyHandle = str ## E.g. uberon, cl; also subset names
Person = str ## ORCID or github handle

@dataclass
class Product(JsonSchemaMixin):
    """
    abstract base class for all products.

    Here, a product is something that is produced by an ontology workflow.
    A product can be manifested in different formats
    """
    id : str
    description: Optional[str] = None
    rebuild_if_source_changes : bool = True

@dataclass
class SubsetProduct(Product):
    """
    Represents an individual subset.
    Examples: goslim_prok (in go), eco_subset (in ro)
    """
    creators : Optional[List[Person]] = None

@dataclass
class ImportProduct(Product):
    """
    Represents an individual import
    Examples: 'uberon' (in go)
    Imports are typically built from an upstream source,
    but this can be configured
    """
    pass

@dataclass
class PatternProduct(Product):
    """
    Represents a DOSDP template
    
    The products here can be CSVs ('parse'ing OWL) or
    they may be OWL (generating)
    """
    pass


@dataclass
class RoboTemplateProduct(Product):
    """
    Represents a ROBOT template
    """
    pass

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
    disabled : bool = False
    rebuild_if_source_changes : bool = True

    def fill_missing(self):
        if self.products is None:
            self.products = []
        if self.ids is not None:
            for id in self.ids:
                if id not in [p.id for p in self.products]:
                    self._add_stub(id)
@dataclass
class SubsetGroup(ProductGroup):
    products : Optional[List[SubsetProduct]] = None

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(SubsetProduct(id=id))

@dataclass
class ImportGroup(ProductGroup):
    products : Optional[List[ImportProduct]] = None

    def _add_stub(self, id : OntologyHandle):
        if self.products is None:
            self.products = []
        self.products.append(ImportProduct(id=id))
    
@dataclass
class PatternGroup(ProductGroup):
    products : Optional[List[PatternProduct]] = None

    
@dataclass
class RoboTemplateGroup():
    products : Optional[List[RoboTemplateProduct]] = None

    
@dataclass
class OntologyProject(JsonSchemaMixin):
    """
    A configuration for an ontology project/repository

    This is divided into project-wide settings, plus
    groups of products. Products are grouped into 4
    categories (more may be added)
    """

    id : OntologyHandle = ""                     ## E.g. uberon, cl
    title : str = ""                             ## 
    repo : str = ""
    github_org : str = ""
    robot_version: Optional[str] = None
    reasoner : str = 'ELK'
    use_dosdps : bool = True
    report_fail_on : Optional[str] = None
    obo_format_options : Optional[str] = None
    uribase : str = 'http://purl.obolibrary.org/obo'
    
    contact : Optional[Person] = None
    creators : Optional[List[Person]] = None
    contributors : Optional[List[Person]] = None

    import_group : Optional[ImportGroup] = None
    subset_group : Optional[SubsetGroup] = None
    pattern_group : Optional[PatternGroup] = None
    robotemplate_group : Optional[RoboTemplateGroup] = None

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

@dataclass
class ExecutionContext(JsonSchemaMixin):
    """
    Top level object that is passed to Jinja2 templates
    """
    project : Optional[OntologyProject] = None
    meta: str = ""

    
@dataclass
class Generator(object):
    context : ExecutionContext = ExecutionContext()

    def generate(self, input='template/src/ontology/Makefile.jinja2'):
        with open(input) as file_:
            template = Template(file_.read())
        return template.render( project = self.context.project)

    def load_config(self,
                    config_file,
                    imports=None,
                    title=None,
                    org=None,
                    repo=None):
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
    

import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-C', '--config', type=click.File('r'))
@click.option('-i', '--input',  type=click.Path(exists=True))
@click.option('-o', '--output')
def create_makefile(config, input, output):
    """
    For testing purposes
    """
    mg = Generator()
    mg.load_config(config)
    print(mg.generate())

@cli.command()
def dump_schema():
    """
    Dumps the python schema as json schema.

    Note: this is intended primarily at odk developers
    """
    import json
    print(json.dumps(OntologyProject.json_schema(), sort_keys=True, indent=4))


@cli.command()
@click.option('-C', '--config',       type=click.File('r'))
@click.option('-T', '--templatedir',  default='./template/')
@click.option('-D', '--outdir',       default='tmp')
@click.option('-d', '--dependencies', multiple=True)
@click.option('-t', '--title',        type=str)
@click.option('-u', '--user',         type=str)
@click.option('-v', '--verbose',      count=True)
@click.argument('repo', nargs=-1)
def seed(config, outdir, templatedir, dependencies, title, user, verbose, repo):
    """
    Seeds an ontology project
    """
    mg = Generator()
    if len(repo) > 0:
        if len(repo) > 1:
            raise Exception('max one repo')
        repo = repo[0]
    else:
        repo = None
    mg.load_config(config,
                   imports=dependencies,
                   title=title,
                   org=user,
                   repo=repo)
    for root, subdirs, files in os.walk(templatedir):
        tdir = root.replace(templatedir,outdir+"/")
        os.makedirs(tdir, exist_ok=True)
        for f in files:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            logging.debug('  {} -> {}'.format(srcf, tgtf))
            copyfile(srcf, tgtf)
        for f in files:
            srcf = os.path.join(root, f)
            tgtf = os.path.join(tdir, f)
            if tgtf.endswith(TEMPLATE_SUFFIX):
                derived_file = tgtf.replace(TEMPLATE_SUFFIX, "")
                with open(derived_file,"w") as s:
                    if f.startswith("_dynamic"):
                        logging.info('  Unpacking: {}'.format(derived_file))
                        unpack_files(tdir, mg.generate(tgtf))
                    else:
                        logging.info('  Compiling: {} -> {}'.format(tgtf, derived_file))
                        s.write(mg.generate(tgtf))

def unpack_files(basedir, txt):
    """
    This unpacks a custom tar-like format in which multiple file paths
    can be specified, separated by ^^^s
    """
    MARKER = '^^^ '
    lines = txt.split("\n")
    f = None
    for line in lines:
        if line.startswith(MARKER):
            path = os.path.join(basedir, line.replace(MARKER, ""))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            f = open(path,"w")
            logging.info('  Unpacking into: {}'.format(path))
        else:
            if f is None:
                if line == "":
                    continue
                else:
                    raise Exception('File marker "{}" required in "{}"'.format(MARKER, line))
            f.write(line + "\n")
            
                
if __name__ == "__main__":
    cli()


