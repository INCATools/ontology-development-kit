# Release artefacts

We made a first stab add defining release artefacts that should cover all use cases community-wide. We need to (1) agree they are all that is needed and (2) they are defined correctly in terms of ROBOT commands. This functionality replaces what was previously done using OORT.

## Terminology:
The **source ontology** is the ontology we are talking about. A **release artefact** is a version of the ontology modified in some specific way, intended for public use. An **import** is a module of an external ontology which contains all the axioms necessary for the source ontology. A **component** is a file containing axioms that belong to the source ontology (but are for one reason or another, like definitions.owl, managed in a separate file). An axiom is said to be **foreign** if it 'belongs' to a different ontology, and **native** if it belongs to the source ontology. For example, the source ontology might have, for one reason or another, been physically asserted (rather than imported) the axiom TransitiveObjectProperty(BFO:000005). If the source ontology does not 'own' the BFO namespace, this axiom will be considered foreign.

There are currently 6 release defined in the ODK:

- base (required)
- full (required)
- non-classified (optional)
- simple (optional)
- basic (optional)
- simple-non-classified (optional, transient)

We discuss all of them here in detail.

# Release artefact 1: base (required)
The base file contains all and only **native** axioms. No further manipulation is performed, in particular no reasoning, redundancy stripping or relaxation. This release artefact is going to be the new backbone of the OBO strategy to combat incompatible imports and consequent lack of interoperability. (Detailed discussions elsewhere, @balhoff has documentation). Every OBO ontology will contain a mandatory base release (should be in the official OBO recommendations as well).
 
The ROBOT command generating the base artefact:
$(SRC): source ontology
$(OTHER_SRC): set of component ontologies
```
$(ONT)-base.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) remove --input $< --select imports  --trim false \
		merge $(patsubst %, -i %, $(OTHER_SRC)) \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@
```
# Release artefact 2: full (required)
The full release artefact contains all logical axioms, including inferred subsumptions. Redundancy stripping (i.e. redundant subclass of axioms) and typical relaxation operations are performed. All imports and components are merged into the full release artefact to ensure easy version management. The full release represents most closely the actual ontology as it was intended at the time of release, including all its logical implications. Every OBO ontology will contain a mandatory full release. 
 
The ROBOT command generating the full artefact:
$(SRC): source ontology
$(OTHER_SRC): set of component ontologies

```
$(ONT)-full.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) merge --input $< \
		reason --reasoner ELK \
		relax \
		reduce -r ELK \ 
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@
```
# Release artefact 3: non-classified (optional)
The non-classified release artefact reflects the 'unmodified state' of the editors file at release time. No operations are performed that modify the axioms in any way, in particular no redundancy stripping. As opposed to the base artefact, both component and imported ontologies are merged into the non-classified release. 

The ROBOT command generating the full artefact:
$(SRC): source ontology
$(OTHER_SRC): set of component ontologies

```
$(ONT)-non-classified.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) merge --input $< \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@
```

# Release artefact 4: simple (optional)

Many users want a release that can be treated as a simple existential graph of the terms defined in an ontology.  This corresponds to the state of  OBO ontologies before logical definitions and imports. For example, the only logical axioms in  -simple release of CL will contain be of the form `CL1 subClassOf CL2` or `CL1 subClassOf R some CL3` where R is any objectProperty and CLn is a CL class.  This role has be fulfilled by the -simple artefact, which up to now has been supported by OORT.

To construct this, we first need to assert inferred classifications,  relax equivalentClass axioms to sets of subClassOf axioms and then strip all axioms referencing foreign (imported) classes.  As ontologies occasionally end up with forieign classes and axioms merged into the editors file, we achieve this will a filter based on obo-namespace.  (e.g. finding all terms with iri matching http://purl.obolibrary.org/obo/CL_{\d}7).

The ROBOT command generating the full artefact:
$(SRC): source ontology
$(OTHER_SRC): set of component ontologies
$(SIMPLESEED): all terms that 'belong' to the ontology

```
$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) \
	reason --reasoner {{ project.reasoner }} --equivalent-classes-allowed {{ project.allow_equivalents }} \
	relax \
	remove --axioms equivalent \
	relax \
	filter --term-file $(SIMPLESEED) --select "annotations ontology anonymous self" --trim true --signature true \
	reduce -r {{ project.reasoner }} \
	annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@
```
NOTES: This requires $(ONTOLOGYTERMS) to include all ObjectProperties usesd.  `--select parents` is required for logical axioms to be retained, but results in a few upper-level classes bleeding through.  We hope this will be fixed by further improvments to Monarch.


# Release artefact 5: basic

Some legacy users (e.g. MGI) require an OBO DAG version of -simple.  OBO files derived from OWL are not guarenteed to be acyclic, but acyclic graphs can be achieved using judicious filtering of relationships (simple existential restrictions) by objectProperty. The -basic release artefact has historically fulfilled this function as part of OORT driven ontology releases. The default -basic version corresponds to the -simple artefact with only 'part of' relationships (BFO:0000050), but others may be added where ontology editors judge these to be useful and safe to add without adding cycles.  We generate by taking the simple release and filtering it

The ROBOT command generating the full artefact:
$(SRC): source ontology
$(OTHER_SRC): set of component ontologies
$(KEEPRELATIONS): all relations that should be preserved.
$(SIMPLESEED): all terms that 'belong' to the ontology

```
$(ROBOT) merge --input $< $(patsubst %, -i %, $(OTHER_SRC)) \
	reason --reasoner {{ project.reasoner }} --equivalent-classes-allowed {{ project.allow_equivalents }} \
	relax \
	remove --axioms equivalent \
	remove --axioms disjoint \
	remove --term-file $(KEEPRELATIONS) --select complement --select object-properties --trim true \
	relax \
	filter --term-file $(SIMPLESEED) --select "annotations ontology anonymous self" --trim true --signature true \
	reduce -r {{ project.reasoner }} \
	annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@
```

# Release artefact 6: simple-non-classified (optional)
This artefact caters to the very special and *hopefully transient* case of some ontologies that do not yet trust reasoning (MP, HP). The simple-non-classified artefact corresponds to the simple artefact, just without the reasoning step.

$(SRC): source ontology
$(OTHER_SRC): set of component ontologies
$(ONTOLOGYTERMS): all terms that 'belong' to the ontology

```
$(ONT)-simple-non-classified.owl: $(SRC) $(OTHER_SRC) $(ONTOLOGYTERMS)
	$(ROBOT) remove --input $< --select imports \
		merge  $(patsubst %, -i %, $(OTHER_SRC))  \
		relax \
		reduce -r ELK \
		filter --term-file $(ONTOLOGYTERMS) --trim true \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ 
```