**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Ontology_Editing_Guide](GO Editor Docs]

## Creating Regulation Terms

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions. 

To create a 'positive regulation of x' or 'negative regulation of x' term, the parent 'regulation of x' term must first be created. To create a parent regulation term: 

1. Make sure the 'Asserted view' is active (not the 'Inferred view'). 

2. In the Protege classes view navigate to ‘biological regulation’
   
3. Click on the add subclass button at the top left corner.
   
4. In the pop-up window add the name of the new regulation term ‘regulation of target process’. The identifier should auto-populate. Click the button to add the term.
   
5. Enter the appropriate information for namespace, definition, synonyms, etc. in the obo editing view as decribed in the 'Creating a New Ontology Term' Section.
   
   Standard definitions for regulation terms: 
   
   - Regulation ```Any process that modulates the frequency, rate or extent of [process]```
   
   - Positive regulation: ```Any process that activates or increases the frequency, rate or extent of [process]```
   
   - Negative regulation: ```Any process that stops, prevents or reduces the frequency, rate or extent of [process]```
   
6. Create a logical definition for the term: ```biological regulation``` __and__ ```regulates``` __some__ ```target process```.
   
7. Remove the asserted ‘biological regulation’ parent.
   
8. Run the reasoner to be sure that reasoning results in the correct inferred parents.

9. Save changes.

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions. 

