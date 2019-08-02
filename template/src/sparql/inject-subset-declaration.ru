PREFIX : <http://www.test.com/ns/test#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT { ?y rdfs:subPropertyOf <http://www.geneontology.org/formats/oboInOwl#SubsetProperty> . }

WHERE {
  ?x <http://www.geneontology.org/formats/oboInOwl#inSubset>  ?y .
}