**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Ontology_Editing_Guide](GO Editor Docs]

### Adding a new Subset (Slim)

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) for creating branches and basic Protégé instructions. 

1.	In the main Protege window, click on the Annotation Properties tab.

2.	Navigate to the ```subset_property``` and select it.

3.	Click on the top left-hand button of the window to add a new subset property.

4.	In the pop-up window add the name of the new slim. The identifier will fill in according to your preferences and will be the next identifier in your set. Click on Refactor in the menu. Select rename entities.

5.	Replace the ```IDSPACE_ identifier``` with the name of your new slim. It is standard to use the same string as when you created the term.

6.	In the annotations tab, click on the ```+```. 

7.	In the pop up window, select ```rdfs:comment```.

8.	In the right hand window, type a small descriptor statement for the slim. Select ```xsd:string``` as the type.

9.	Click OK to save the changes. You should now see the comment field in the annotations tab.

See [Daily Workflow](http://ontology-development-kit.readthedocs.io/en/latest/index.html#daily-workflow) section for commit, push and merge instructions. 
