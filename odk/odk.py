"""
Generate artefacts (Makefile, default ontology edit file, imports) from a project configuration

See https://github.com/ontodev/robot/issues/37

SUBJECT TO CHANGE!

To test:

python3 odk/odk.py create_makefile -c examples/envo.yaml
"""
from typing import Optional, Set, List, Union, Dict, Any
from dataclasses import dataclass, field
from jinja2 import Template
from dacite import from_dict
import yaml

# Primitive Types
OntologyHandle = str ## E.g. uberon, cl; also subset names
Person = str ## ORCID or github handle

@dataclass
class Product(object):
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
class ProductGroup(object):
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
class OntologyProject(object):
    """
    A configuration for an ontology project/repository

    This is divided into project-wide settings, plus
    groups of products. Products are grouped into 4
    categories (more may be added)
    """

    id : OntologyHandle = "" ## E.g. uberon, cl
    title : str = ""
    repo : str = ""
    github_org : str = ""
    robot_version: Optional[str] = None
    reasoner : str = 'ELK'
    use_dosdps : bool = True
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
class ExecutionContext(object):
    """
    Top level object that is passed to Jinja2 templates
    """
    project : Optional[OntologyProject] = None
    meta: str = ""

    
@dataclass
class Generator(object):
    context : ExecutionContext = ExecutionContext()

    def generate(self, input='template/src/ontology/Makefile.jinja2'):
        print(self.context.project)
        with open(input) as file_:
            template = Template(file_.read())
        return template.render( project = self.context.project)

    def load_config(self, config_file):
        obj = yaml.load(config_file)
        project = from_dict(data_class=OntologyProject, data=obj)
        project.fill_missing()
        self.context = ExecutionContext(project=project)
    

import click

@click.group()
def cli():
    pass

@cli.command()
#@click.option("config", "-c", type=click.Path(exists=True))
@click.option("config", "-c", type=click.File('r'))
@click.option("input", "-i", type=click.Path(exists=True))
@click.option("output", "-o")
def create_makefile(config, input, output):
    mg = Generator()
    mg.load_config(config)
    print(mg.context)
    print(mg.generate())

if __name__ == "__main__":
    cli()


