PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>


#DELETE {
#  ?ontology ?ontology_annotation_property ?ontology_annotation_value .
#}

INSERT { 
    ?ontology dc:source ?version_iri .
}

WHERE {
  ?ontology rdf:type owl:Ontology ;
        owl:versionIRI ?version_iri .
  #OPTIONAL {
  #  ?ontology ?ontology_annotation_property ?ontology_annotation_value .
  #}

}