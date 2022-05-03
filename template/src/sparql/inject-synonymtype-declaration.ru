PREFIX : <http://www.test.com/ns/test#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT { ?y rdfs:subPropertyOf <http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty> . }

WHERE {
  ?x <http://www.geneontology.org/formats/oboInOwl#hasSynonymType>  ?y .
  FILTER(isIRI(?y))
  FILTER(regex(str(?y),"^(http://purl.obolibrary.org/obo/)") || regex(str(?y),"^(http://www.ebi.ac.uk/efo/)") || regex(str(?y),"^(https://w3id.org/biolink/)"))
}