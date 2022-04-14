**NOTE** This documentation is incomplete, for now you may be better consulting the [GO Editor Docs](http://wiki.geneontology.org/index.php/Ontology_Editing_Guide)

# Merging Ontology Terms

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions. 

**Note** Before performing a merge, make sure that you know all of the consequences that the merge will cause. In particular, be sure to look at child terms and any other terms that refer to the ‘deprecated’ term. In many cases a simple merge of two terms is not sufficient because it will result in equivalent classes for child terms. For example if deprecated term X is going to be merged into target term Y and ‘regulation of X’ and ‘regulation of Y’ terms exist, then you will need to merge the regulation terms in addition to the primary terms. You will also need to edit any terms that refer to the deprecated term to be sure that the names and definitions are consistent.

## Manual Workflow

1.	**Find the ID of the term in which the deprecated term will be merged** 
    - Navigate to 'winning' term using the Search box. **Copy the ID of the winning term somewhere.**  
    
 2. **Duplicate annotations from the deprecated terms**
    - Navigate to the term to be deprecated.  
    - Right click on it and select ```Duplicate class``` then OK in the pop up window. This should create a class with the exact same name. 
    - On the duplicated class (you can see this by (CL:XXXX) within your range added), right click and select ```Change IRI (Rename)```
    - Copy the ID of the winning term (obtained in Step 1).
    - Be sure to use the underscore ```_``` in the identifier instead of the colon ```:```, for example: ```GO_1234567```. Make sure that the 'change all entities with this URI' box is checked.  
    - Navigate to the winning term IRI, all annotations should be merged.

3. **Change deprecated term label to a synonym**
    - In the annotations box of the winning term there are now two terms with labels 'rdfs:label'. Click the ```o``` to change the label of the  deprecated term.     
    - In the resulting pop-up window, select the appropriate synonym label from the list on the left:
      1.	```has_broad_synonym```
      2.	```has_exact_synonym```
      3.	```has_narrow_synonym```
      4.	```has_related_synonym``` (if unsure, this is the safest choice)

4.  **Remove duplicated or inappropriate annotations**
    - Check the definition, if there are multiple entries, remove the deprecated one by clicking on the ```x``` on the right.
    - Check the subclasses and remove inappropriate/duplciated ones by clicking on the ```x``` on the right.
    - Check list of synonyms and remove inappropriate/duplciated ones by clicking on the ```x``` on the right. 
    - Note down the created_by and created_date (there can only be one value per term for each of these fields; this will be useful if you need to pick one after the merge is done).

5. **Obsolete old term**
    - Deprecate/obsolete the old term by following instructions found in [Obsoleting an Existing Ontology Term] (https://ontology-development-kit.readthedocs.io/en/latest/ObsoleteTerm.html).
    - Ensure that you add a ```rdfs:comment``` that states that term was duplicated and to refer to the new new.
    - Ensure that you add a ```term replaced by``` annotations as per the instructions and add the winning merged term.
   
6. **Synchronize the reasoner** and make sure there are no terms that have identical definitions as a result of the merge. These are displayed with an 'equivalent' sign `≡` in the class hierarchy view on the left hand panel.   

7. Save changes. 

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions. 

## Merge using owltools

This is the workflow that is used in [Mondo](https://mondo.readthedocs.io/en/latest/editors-guide/merging-and-obsoleting/).

1. Create a branch and name it issue-### (for example issue-2864)
1. Open Protege
1. Prepre the owltools command:
`owltools --use-catalog mondo-edit.obo  --obsolete-replace [CURIE 1] [CURIE 2] -o -f obo mondo-edit.obo`  

CURIE 1 = term to be obsoleted  
CURIE 2 = replacement term (ie term to be merged with)

For example:
If to merge MONDO:0023052 ectrodactyly polydactyly with MONDO:0009156 ectrodactyly-polydactyly syndrome, the command is: 

`owltools --use-catalog mondo-edit.obo  --obsolete-replace MONDO:0023052 MONDO:0009156 -o -f obo mondo-edit.obo`

1. In Terminal, navigate to your ontology directory: src/ontology
1. Run your owltools command
1. Check the output in GitHub desktop
1. Open a new version of your ontology edit file in Protege
1. Search for the term that was obsoleted
1. Add SeeAlso with a link to the GitHub issue that requested the obsoletion.
1. Add an obsoletion reason: use the annotation property 'has obsolescence reason' and write 'terms merged' in the literal field.
1. Search for the 'term replaced by' term
1. Delete the old ID
1. Review the annotations to ensure there are no duplicate annotations. If there are, they should be merged.
1. Review the subClassOf assertions, and make sure there are no duplicates. If there are, they should be merged.
1. When reviewing the diff, make sure there is not an Alt ID. The diff should only show additions to the merged term and the obsoletion

----
TROUBLESHOOTING: Travis/Jenkins errors
1. **Merging a term that is used as 'replaced by' for an obsolete term**
  ``` :: ERROR: ID-mentioned-twice:: GO:0030722
       :: ERROR: ID-mentioned-twice:: GO:0048126 
         GO:0030722 :: ERROR: has-definition: missing definition for id
   ```
The cause of this error is that Term A (GO:0048126) was obsoleted and had replace by Term B (GO:0030722). The GO editor tried to merge Term B into a third term term C (GO:0007312). The Jenkins checkk failed because 'Term A replaced by' was an alternative_id rather than by a main_id. 
Solution: In the ontology, go to the obsolete term A and replace the Term B by term C to have a primary ID as the replace_by. 

