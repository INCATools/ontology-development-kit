# Formatting your ontology annotations correctly

The new OBO Foundry guidelines encourage the annotation of ontologies with an appropriately formatted description, title and license. Here are some examples that can be used as a guide to implement those in your ontology.

## RDF/XML Example:

```
<?xml version="1.0"?>
<rdf:RDF xmlns="http://purl.obolibrary.org/obo/license.owl#"
     xml:base="http://purl.obolibrary.org/obo/license.owl"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:terms="http://purl.org/dc/terms/">
    <owl:Ontology rdf:about="http://purl.obolibrary.org/obo/license.owl">
        <dc:description rdf:datatype="http://www.w3.org/2001/XMLSchema#string">An integrated and fictional ontology for the description of abnormal tomato phenotypes.</dc:description>
        <dc:title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Tomato Phenotype Ontology (TPO)</dc:title>
        <terms:license rdf:resource="https://creativecommons.org/licenses/by/3.0/"/>
    </owl:Ontology>
    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/description"/>
    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/title"/>
    <owl:AnnotationProperty rdf:about="http://purl.org/dc/terms/license"/>
</rdf:RDF>
```

## Functional Syntax Example:

```
Prefix(:=<http://purl.obolibrary.org/obo/license.owl#>)
Prefix(owl:=<http://www.w3.org/2002/07/owl#>)
Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)
Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)
Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)


Ontology(<http://purl.obolibrary.org/obo/license.owl>
Annotation(<http://purl.org/dc/elements/1.1/description> "An integrated and fictional ontology for the description of abnormal tomato phenotypes."^^xsd:string)
Annotation(<http://purl.org/dc/elements/1.1/title> "Tomato Phenotype Ontology (TPO)"^^xsd:string)
Annotation(<http://purl.org/dc/terms/license> <https://creativecommons.org/licenses/by/3.0/>)

)
```

## OWL/XML Example:

```
<?xml version="1.0"?>
<Ontology xmlns="http://www.w3.org/2002/07/owl#"
     xml:base="http://purl.obolibrary.org/obo/license.owl"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     ontologyIRI="http://purl.obolibrary.org/obo/license.owl">
    <Prefix name="" IRI="http://purl.obolibrary.org/obo/license.owl#"/>
    <Prefix name="owl" IRI="http://www.w3.org/2002/07/owl#"/>
    <Prefix name="rdf" IRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>
    <Prefix name="xml" IRI="http://www.w3.org/XML/1998/namespace"/>
    <Prefix name="xsd" IRI="http://www.w3.org/2001/XMLSchema#"/>
    <Prefix name="rdfs" IRI="http://www.w3.org/2000/01/rdf-schema#"/>
    <Annotation>
        <AnnotationProperty IRI="http://purl.org/dc/elements/1.1/description"/>
        <Literal>An integrated and fictional ontology for the description of abnormal tomato phenotypes.</Literal>
    </Annotation>
    <Annotation>
        <AnnotationProperty IRI="http://purl.org/dc/elements/1.1/title"/>
        <Literal>Tomato Phenotype Ontology (TPO)</Literal>
    </Annotation>
    <Annotation>
        <AnnotationProperty abbreviatedIRI="terms:license"/>
        <IRI>https://creativecommons.org/licenses/by/3.0/</IRI>
    </Annotation>
    <Declaration>
        <AnnotationProperty IRI="http://purl.org/dc/elements/1.1/title"/>
    </Declaration>
    <Declaration>
        <AnnotationProperty IRI="http://purl.org/dc/elements/1.1/description"/>
    </Declaration>
    <Declaration>
        <AnnotationProperty IRI="http://purl.org/dc/terms/license"/>
    </Declaration>
</Ontology>
```

## OBO Example:

```
format-version: 1.2
ontology: license
property_value: http://purl.org/dc/elements/1.1/description "An integrated and fictional ontology for the description of abnormal tomato phenotypes." xsd:string
property_value: http://purl.org/dc/elements/1.1/title "Tomato Phenotype Ontology (TPO)" xsd:string
property_value: http://purl.org/dc/terms/license https://creativecommons.org/licenses/by/3.0/
```
