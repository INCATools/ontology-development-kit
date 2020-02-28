**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Ontology_Editing_Guide](GO Editor Docs]

# Term Comments

## Adding Comments to Terms

Comments may be added to ontology terms to further explain their intended usage.

Wherever possible, we strive to use standard language for similar types of comments and suggest alternative terms to use. 

Some examples of comments, and standard language for their usage, are:

## Do Not Annotate
This term should not be used for direct annotation.  It should be possible to make a more specific annotation to one of the children of this term. 

Example:
GO:0006810 transport 

Note that this term should not be used for direct annotation. It should be possible to make a more specific annotation to one of the children of this term, for e.g. transmembrane transport, microtubule-based transport, vesicle-mediated transport, etc. 

## Do Not Manually Annotate
This term should not be used for direct manual annotation.  It should be possible to make a more specific manual annotation to one of the children of this term.   

Example:
GO:0000910 cytokinesis

Note that this term should not be used for direct annotation. When annotating eukaryotic species, mitotic or meiotic cytokinesis should always be specified for manual annotation and for prokaryotic species use 'FtsZ-dependent cytokinesis; GO:0043093' or 'Cdv-dependent cytokinesis; GO:0061639'.  Also, note that cytokinesis does not necessarily result in physical separation and detachment of the two daughter cells from each other.
