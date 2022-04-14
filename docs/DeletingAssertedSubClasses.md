**NOTE** This documentation is incomplete, for now you may be better consulting the [GO Editor Docs](http://wiki.geneontology.org/index.php/Ontology_Editing_Guide)

### Deleting Asserted Subclasses

Asserted is_a parents do not need to be retained as entries in the 'SubClass of' section of the Description window in Protege
if the logical definition for a term results in their inference.

If you have created a logical defintion for your term, you can delete the asserted is_a parent by clicking on the X to the
right term.

Once you synchronize the Reasoner, you will see the reasoned classification of your new term, including the inferred is_a 
parent(s).

If the inferred classification does not contain the correct parentage, or doesn't make sense, then you will need to modify the 
logical definition.

If an existing term contains a logical definition and still shows an asserted is_a parent in the 'SubClass of' section, you
may delete that asserted parent, as well.  Just make sure to run the Reasoner to check that the asserted parent is now
replaced with the correct reasoned parent(s).
