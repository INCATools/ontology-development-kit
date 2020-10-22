**NOTE** This documentation is incomplete, for now you may be better consulting the [GO Editor Docs](http://wiki.geneontology.org/index.php/Ontology_Editing_Guide)

# Merging Ontology Terms

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions. 

**Note** Before performing a merge, make sure that you know all of the consequences that the merge will cause. In particular, be sure to look at child terms and any other terms that refer to the ‘deprecated’ term. In many cases a simple merge of two terms is not sufficient because it will result in equivalent classes for child terms. For example if deprecated term X is going to be merged into target term Y and ‘regulation of X’ and ‘regulation of Y’ terms exist, then you will need to merge the regulation terms in addition to the primary terms. You will also need to edit any terms that refer to the deprecated term to be sure that the names and definitions are consistent.

1.	**Find the ID of the term in which the deprecated term will be merged** 
    - Navigate to 'winning' term using the Search box. **Copy the ID of the winning term somewhere.**  
    
 2. **Remove annotations from the deprecated terms**
    - Navigate to the term to be deprecated.  
    - Remove the logical definition by clicking on the ```x``` on the right.
    - Remove all subclasses by clicking on the ```x``` on the right.
    - Look at the definition; if it does not seem relevant, remove it by clicking on the ```x``` on the right; otherwise copy/paste it somewhere to refer to when reviewing the definition for the winning term.
    - Note down the created_by and created_date (there can only be one value per term for each of these fields; this will be useful if you need to pick one after the merge is done).
    - Check existing list of synonyms to see if they need to be moved to the new term, otherwise delete them by clicking on the ```x``` on the right.  
      
3.  **Change the ID of the term to be deprecated to the winning term's ID**
    - In the term to be deprecated, click on Refactor > Rename entity’ in the Protege menu (shortcut: ```command-U```) 
    - Copy the ID of the winning term (obtained in Step 1). 
    - Be sure to use the underscore ```_``` in the identifier instead of the colon ```:```, for example: ```GO_1234567```. Make sure that the 'change all entities with this URI' box is checked.  
 
 4. **Make the deprecated ID an 'alternative ID'**
    - Navigate to the winning term. In the Annotations box, locate the ID of the deprecated term. Click the ```o``` to change the ID type. 
    - In the resulting pop-up window, making sure the 'Literal' tab is selected in the top right side box, select ```has_alternative_id``` from the list on the left side. Double check that the entry corresponds to the GO ID of the deprecated term.  
    - Click 'OK'. The deprecated term identifier should now have the label ```has_alternative_id``` instead of ```id```.  

5. **Change deprecated term label to a synonym**
    - In the annotations box of the winning term there are now two terms with labels 'rdfs:label'. Click the ```o``` to change the label of the  deprecated term.     
    - In the resulting pop-up window, select the appropriate synonym label from the list on the left:
      1.	```has_broad_synonym```
      2.	```has_exact_synonym```
      3.	```has_narrow_synonym```
      4.	```has_related_synonym``` (if unsure, this is the safest choice)

6. **Fix synonyms** 
    - In the annotations box of the winning term, check the list of synonyms to see if they are all still make appropriate.  

7. If needed, fix the definition, using information from the deprecated term as appropriate.  

7. **Synchronize the reasoner** and make sure there are no terms that have identical definitions as a result of the merge. These are displayed with an 'equivalent' sign `≡` in the class hierarchy view on the left hand panel.   

8. Save changes. 

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions. 

----
TROUBLESHOOTING: Travis/Jenkins errors
1. **Merging a term that is used as 'replaced by' for an obsolete term**
  ``` :: ERROR: ID-mentioned-twice:: GO:0030722
       :: ERROR: ID-mentioned-twice:: GO:0048126 
         GO:0030722 :: ERROR: has-definition: missing definition for id
   ```
The cause of this error is that Term A (GO:0048126) was obsoleted and had replace by Term B (GO:0030722). The GO editor tried to merge Term B into a third term term C (GO:0007312). The Jenkins checkk failed because 'Term A replaced by' was an alternative_id rather than by a main_id. 
Solution: In the ontology, go to the obsolete term A and replace the Term B by term C to have a primary ID as the replace_by. 

