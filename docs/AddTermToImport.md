**NOTE** This documentation is incomplete, for now you may be better consulting the [GO Editor Docs](http://wiki.geneontology.org/index.php/Ontology_Editing_Guide)

### Adding Terms to the Import Files

Terms are imported to GO from other ontologies, but not all terms from external ontologies are imported. Occasionally, you will find that a valid identifier exists in an external ontology, but the identifier is not available in Protege because that term is not yet imported. To import a term from an external ontology:

1.	Navigate to the imports folder on GitHub, located at [https://github.com/geneontology/go-ontology/tree/master/src/ontology/imports](https://github.com/geneontology/go-ontology/tree/master/src/ontology/imports).
2.	Look in the list of ontologies for the ontology that contains the term you wish to import.
3.	Identify the ```ontology_terms.txt``` file for the target ontology. For example, for the addition of a new taxon, the file can be found at [https://github.com/geneontology/go-ontology/blob/master/src/ontology/imports/ncbitaxon_terms.txt](https://github.com/geneontology/go-ontology/blob/master/src/ontology/imports/ncbitaxon_terms.txt).
4.	Click on the icon of a pencil in the upper right corner of the window to edit the file.
5.	Add the new term on the next available line at the bottom of the file.
6.	Click preview changes.
7.	You can now either commit the file directly to master or create a branch and a pull request as described before.
