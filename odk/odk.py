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
    hold by default for all within that group
    """
    ids : Optional[List[OntologyHandle]] = None
    disabled : bool = False
    rebuild_if_source_changes : bool = True

@dataclass
class SubsetGroup(ProductGroup):
    subsets : Optional[List[SubsetProduct]] = None

@dataclass
class ImportGroup(ProductGroup):
    imports : Optional[List[ImportProduct]] = None

@dataclass
class PatternGroup(ProductGroup):
    patterns : Optional[List[PatternProduct]] = None

@dataclass
class RoboTemplateGroup():
    robotemplates : Optional[List[RoboTemplateProduct]] = None


    
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


