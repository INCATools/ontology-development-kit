
# Initial Setup

## Installing Protege

1. Follow the instructions on the GO wiki page: [http://wiki.geneontology.org/index.php/Protege_setup_for_GO_Eds](http://wiki.geneontology.org/index.php/Protege_setup_for_GO_Eds)

2. _Need to add more here about the different Views and Tabs needed for working._


## ID Ranges

1. Curators and projects are assigned specific ID ranges within the prefix for your ontology. See the README-editors.md for your ontology

2. An example: [go-idranges.owl](https://github.com/geneontology/go-ontology/blob/master/src/ontology/go-idranges.owl)

3. __NOTE:__ You should only use IDs within your range.

4. If you have only just set up this repository, modify the idranges file and add yourself or other editors. 


## Setting ID ranges in Protege

1. Once you have your assigned ID range, you need to configure Protege so that your ID range is recorded in the Preferences menu.  Protege does not read the idranges file.

2. In the Protege menu, select Preferences.

3. In the resulting pop-up window, click on the New Entities tab and set the values as follows.

4. In the Entity IRI box:
    
    __Start with:__ Specified IRI: [http://purl.obolibrary.org/obo](http://purl.obolibrary.org/obo)

    __Followed by:__ ```/```

    __End with:__ ```Auto-generated ID```

5. In the Entity Label section:

    __Same as label renderer:__ IRI: [http://www.w3.org/2000/01/rdf-schema#label](http://www.w3.org/2000/01/rdf-schema#label)

6.  In the Auto-generated ID section:

    * Numeric

    * Prefix `GO_`

    * Suffix: _leave this blank_

    * Digit Count `7`

    * __Start:__ see [go-idranges.owl](https://github.com/geneontology/go-ontology/blob/master/src/ontology/go-idranges.owl). Only paste the number after the ```GO:``` prefix.  Also, note that when you paste in your GO ID range, the number will automatically be converted to a standard number, e.g. pasting 0110001 will be converted to 110,001.)

    * __End:__ see [go-idranges.owl](https://github.com/geneontology/go-ontology/blob/master/src/ontology/go-idranges.owl)

    * Remember last ID between Protege sessions: ALWAYS CHECK THIS

    (__Note:__ You want the ID to be remembered to prevent clashes when working in parallel on branches.)
