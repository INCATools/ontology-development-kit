
See also [GO Editors Guide on Obsoletion])http://wiki.geneontology.org/index.php/Obsoleting_an_Existing_Ontology_Term)

# Obsoleting an Existing Ontology Term

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions.

1. Check if the term (or any of its children) is being used for annotation: 
   - Go to AmiGO, search for the term, either by label or ID
   - Use filters on the left to look at direct annotations, EXP annotation, InterPro2GO annotations
   - Notify affected groups

2. Check if the term is used elsewhere in the ontology
   - In Protégé, go to the 'Usage' tab to see if that ID is used elsewhere. Search for the term name or the term IRI (ie with underscore between GO and the numerical part of the ID, for example: '''GO_0030722'''
   - If the term is a parent to other terms or is used in logical definitions, make sure that another term replaces the obsolete term

3. Send a notification email. 
Template: 
   - SUBJECT: Proposal to obsolete [GO:ID] [GO term name]
   - BODY: Dear all,  The proposal has been made to obsolete: [GO:ID] [GO term name]. 
   The reason for obsoletion is [SPECIFY]. 
   There are X experimental annotations to this term. 
   There are X InterPro2GO mappings to this term. 
   Any comments can be added to the issue: [link to GitHub ticket]. We are opening a comment period for this proposed obsoletion. We'd like to proceed and obsolete this term on [7 days after the message; unless it involves a lot of reannotation, in this case it can be longer] 
   *** Unless objections are received by [DATE] , we will assume that you agree to this change. ***

**Remember to list the databases affected by the obsoletion and tag people in the GH ticket**
**Check go-slims**

**Possible reasons for obsoletions:** 
* The reason for obsoletion is that there is no evidence that this function/process/component exists. (eg: GO:0019562 L-phenylalanine catabolic process to phosphoenolpyruvate; GO:0097605 regulation of nuclear envelope permeability’; GO:0015993 molecular hydrogen transport)
* The reason for obsoletion is that the term is not clearly defined and usage has been inconsistent (eg: GO:0030818 negative regulation of cAMP biosynthetic process)
* The reason for obsoletion is that this term represent a GO-CAM model. (eg: GO:0072317 glucan endo-1,3-beta-D-glucosidase activity involved in ascospore release from ascus; GO:0100060 negative regulation of SREBP signaling pathway by DNA binding)
* The reason for obsoletion is that this term represent an assay and not a real process. (eg: GO:0035826	rubidium ion transport)
* The reason for obsoletion is that the data from the paper for which the term was requested can be accurately described using [appropriate GO term]. (eg: GO:0015032 storage protein import into fat body)
* etc 



OBSOLETION PROCESS 
1. Navigate to the term to be obsoleted.
 
2. Make the status of the term obsolete: 

   1. In the 'Annotations' window, click on the ```+``` sign next to 'Annotations'.
   2. In the resulting pop-up window, select ```owl:deprecated``` from the left-hand menu.
   3. Make sure the 'Literal' tab view is selected from the right-hand tab list. Type ```true``` in the text box.
   4. In the 'Type' drop-down menu underneath the text box, select ```xsd:boolean```  
   5. Click OK.  You should now see the term crossed out in the Class hierarchy view.

3. Remove equivalence axiom:  In the 'Description' window, under the 'Equivalent To', click the ```x``` on the right-hand side to delete the logical definition. 
 
4. Remove 'SubClass Of' relations: In the 'Description' window, under the 'SubClass Of' entry, click the ```x``` on the right-hand side to delete the SubClass Relation.  
 
5. Add ‘obsolete’ to the term name: In the 'Annotations' window, click on the ```o``` on the right-hand side of the rdfs:label entry to edit the term string. In the resulting window, in the Literal tab, in front of the term name, type: ```obsolete```
For example: ```obsolete gamma-glutamyltransferase activity```
 __Note the case-sensitivity. Make sure to have a space (and no other character) between 'obsolete' and the term label__.   
  
5. Add ‘OBSOLETE’ to the term definition: In the 'Description' window, click on the ```o``` on the right-hand side of the definition entry. In the resulting window, in the Literal tab, at the beginning of the definition, type: ```OBSOLETE.``` 
For example: ```OBSOLETE. Catalysis of the reaction: (5-L-glutamyl)-peptide + an amino acid = peptide + 5-L-glutamyl-amino acid.```
 __Note the case-sensitivity__.   
 
6. Add a statement about why the term was made obsolete: In the 'Annotations' window, select ```+``` to add an annotation. In the resulting menu, select ```rdfs:comment``` and select Type:  ```Xsd:string```.
Consult the wiki documentation for suggestions on standard comments:
      
     - [http://wiki.geneontology.org/index.php/Curator_Guide:_Obsoletion](http://wiki.geneontology.org/index.php/Curator_Guide:_Obsoletion)
      
     - [http://wiki.geneontology.org/index.php/Obsoleting_GO_Terms](http://wiki.geneontology.org/index.php/Obsoleting_GO_Terms)
      
     - [http://wiki.geneontology.org/index.php/Editor_Guide](http://wiki.geneontology.org/index.php/Editor_Guide)
 
7. If the obsoleted term was replaced by another term in the ontology: In the 'Annotations' window, select ```+``` to add an annotation. In the resulting menu, select ```term replaced by``` and enter the ID of the replacement term.  
 
8. If the obsoleted term was not replaced by another term in the ontology, but there are existing terms that might be appropriate for annotation, add those term IDs in the 'consider' tag: In the 'Annotations' window, select ```+``` to add an annotation. In the resulting menu, select ```consider``` and enter the ID of the replacement term.  

9. Save changes. 
    
See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions. 
