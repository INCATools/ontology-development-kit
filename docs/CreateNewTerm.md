**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Ontology_Editing_Guide](GO Editor Docs]

# Creating a New Ontology Term

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions.

1. To create a new term, the 'Asserted view' must be active (not the 'Inferred view'). 

2. In the Class hierarchy window, click on the 'Add subclass' button at the upper left of the window.

3. A pop-up window will appear asking you to enter the Name of the new term. When you enter the term name, you will see your ID automatically populate the IRI box. Once you have entered the term, click 'OK' to save the new term. You will see it appear in the class hierarchy. 

4. Navigate to the OBO annotation window. 

5. In the OBO annotation window add:

    1. Namespace
       1. Begin typing one of the three branches (autocomplete will guide you to the correct term):
               - ```biological_process```
               - ```cellular _component```
               - ```molecular_function```
       2. For Type, select: ```xsd:string```
           
    2. Definition
       1. Click on the  ```+``` next to the Definition box
       2. Add the textual definition in the pop-up box.
       3. For Type, select: ```Xsd:string```
       4. Click OK.
       
     3. Add Definition References
        1. Click on the circle with the ‘Ref’ in it next to add Definition References and in the resulting pop-up click on the ```+``` to add a new ref, making sure they are properly formatted with a database abbreviation followed by a colon, followed by the text string or ID. Examples: ```GOC:bhm, PMID:27450630```.
         2. Select Type: ```xsd:string``` 
         3. Click OK.
         4. Add each definition reference separately by clicking on the ```+``` sign.
	 
      4. Add synonyms and dbxrefs following the same procedure if they are required for the term.
6. If you have created a logical definition for your term, you can delete the asserted ```is_a``` parent in the ‘subclass of’ section. Once you synchronize the reasoner, you will see the automated classification of your new term. If the inferred classification doesn’t make sense, then you will need to modify the logical definition. 

	```
    Protege tip:  If you need to create a logical definition using a GO term name that does not begin 
    with an alphabetic character, e.g. GO:0004534 (5'-3' exoribonuclease activity), navigate to the 
    View menu in Protege and select 'Render by entity IRI short name (Id).  This will allow you to 
    enter a logical definition by entering the relations and term as IDs, e.g. RO_0002215 some GO_0004534.  
    Note the use of the underscore instead of the colon in the ID.  You can then return to the View 
    menu to switch back to Render by label (rdfs:label) to see the term names.
	```

7. In some cases such as ```part_of``` relations based on external partonomies, it might be necessary to assert the ```part_of``` relationships. For example: ```‘heart valve development’ part_of some ‘heart development’```. In those cases, it is important to browse the external ontologies to be sure that nothing is missing. 

8. When you have finished adding the term, you can hover over it in the class window to reveal its GO_id.

9. Save the file and ___return to your terminal window___. Then, type: ```git status```. This will confirm which file has been modified. 

10. To see how the branch was modified, type: ```git diff```. In this case, go-edit.obo was modified. The text below is not the entire diff for this edit, but is an example. If the diff is very large, you will need to hit a space to continue to see it and then hit ‘q’ to get back to the prompt at the end of the diff file. 
 
     ```
     ~/repos/MY-ONTOLOGY/src/ontology(issue-13390) $ git diff
     diff --git a/src/ontology/go-edit.obo b/src/ontology/go-edit.obo
     index 72ae7e9..8d47fa1 100644
     --- a/src/ontology/go-edit.obo
     +++ b/src/ontology/go-edit.obo
     @@ -400751,6 +400751,85 @@ created_by: dph
      creation_date: 2017-04-28T12:39:13Z
      
      [Term]
     +id: GO:0061868
     +name: hepatic stellate cell migration
     +namespace: biological_process
     +def: "The orderly movement of a hepatic stellate cell from one site to another." [PMID:24204762]
     +intersection_of: GO:0016477 ! cell migration
     +intersection_of: results_in_movement_of CL:0000632 ! hepatic stellate cell
     +created_by: dph
     +creation_date: 2017-05-01T13:01:40Z
     +
     +[Term]
      id: GO:0065001
      name: specification of axis polarity
      namespace: biological_process
     ~/repos/MY-ONTOLOGY/src/ontology(issue-13390) $
     ``` 
 
See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions.
