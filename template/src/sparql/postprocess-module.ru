PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


DELETE {
  ?ontology ?ontology_annotation_property ?ontology_annotation_value ;
      owl:versionIRI ?version_iri .
}

INSERT { 
    ?subset rdfs:subPropertyOf <http://www.geneontology.org/formats/oboInOwl#SubsetProperty> . 
    ?ontology dc:source ?version_iri .
}

WHERE {
  ?x <http://www.geneontology.org/formats/oboInOwl#inSubset>  ?subset .
  OPTIONAL {
    ?ontology rdf:type owl:Ontology ;
        owl:versionIRI ?version_iri .
  }
  OPTIONAL {
    ?ontology rdf:type owl:Ontology ;
        ?ontology_annotation_property ?ontology_annotation_value .
  }

}