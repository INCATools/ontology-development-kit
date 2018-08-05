# ----------------------------------------
# Makefile for foobar
# Generated using ontology-starter-kit
# ----------------------------------------
# <do not edit above this line>

# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://purl.obolibrary.org/obo
ONT=foobar
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
RELEASEDIR=../..
ROBOT= robot
OWLTOOLS= owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
DOSDP_SCHEMA=http:// # change to PURL when ready.
PATTERN_TESTER=simple_pattern_tester.py
DOSDPT=dosdp-tools

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: all_imports sparql_test patterns $(ONT).owl $(ONT).obo 
test: sparql_test all
prepare_release: all
	cp $(ONT).owl $(ONT).obo $(RELEASEDIR) &&\
	mkdir -p $(RELEASEDIR)/imports &&\
	cp imports/*.owl $(RELEASEDIR)/imports &&\
	cp imports/*.obo $(RELEASEDIR)/imports &&\
	git add $(RELEASEDIR)/imports/*.obo &&\
	git add $(RELEASEDIR)/imports/*.owl &&\
	(test -f subsets/*owl && cp subsets/* $(RELEASEDIR)/subsets && git add $(RELEASEDIR)/subsets/* || echo "no subsets") &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"
 
# ----------------------------------------
# Main release targets
# ----------------------------------------

# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
$(ONT).owl: $(SRC)
	$(ROBOT)  reason -i $< -r ELK relax reduce -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = MY_IMPORTS_LIST
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_import.obo,$(IMPORTS)) $(patsubst %, imports/%_terms.txt,$(IMPORTS))

# generate seed with all referenced entities

ed_definitions_merged.owl: $(SRC) ../patterns/definitions.owl
	$(ROBOT) merge -i $(SRC) -i ../patterns/definitions.owl -o $@

seed.txt: ed_definitions_merged.owl
	$(ROBOT) query -f csv -i $< --query ../sparql/terms.sparql $@

# Generate terms.txt for each import.  # Assume OBO-style Possibly hacky step?
# Should be able to drop this if robot can just take a big messy list of terms as input.

imports/%_terms_combined.txt: seed.txt
	cat $< imports/$*_terms.txt | sort | uniq >  $@

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms_combined.txt
	$(ROBOT) extract -i $< -T imports/$*_terms_combined.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

# convert imports to obo.
# this can be useful for spot-checks and diffs.
# we set strict mode to false by default. For discussion see https://github.com/owlcs/owlapi/issues/752
imports/%_import.obo: imports/%_import.owl
	$(ROBOT) convert --check false -i $< -f obo -o $@.tmp && mv $@.tmp $@

# clone remote ontology locally, perfoming some excision of relations and annotations
mirror/%.owl: $(SRC)
	$(ROBOT) convert -I $(OBO)/$*.owl -o $@
.PRECIOUS: mirror/%.owl

# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT).obo
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels

# Only needed until robot supports catalogs



#  run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	robot verify  --catalog catalog-v001.xml -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
 # ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	robot query -f tsv -i $< $(REPORT_ARGS)

# ----------------------------------------
# Docker (experimental)
# ----------------------------------------
IM=build-$(ONT)
build-docker:
	docker build -t $(ONT) .

# ----------------------------------------
# Patterns (experimental)
# ----------------------------------------

# Test patterns for schema compliance:


PATTERN_IMPORTS = ../patterns/pattern.owl $(patsubst %, ../patterns/imports/%_import.owl,$(IMPORTS))

# Better to make this an intermediate & merge with pattern.owl file having correct iri and import statements - configured by make

../patterns/pattern.owl: pattern_schema_checks
	$(DOSDPT) prototype --obo-prefixes --template=../patterns --outfile=$@

pattern_schema_checks:
	simple_pattern_tester.py ../patterns/ # 2>&1 | tee $@

../patterns/imports/seed.txt: ../patterns/pattern.owl
	$(ROBOT) query -f csv -i $< --query ../sparql/terms.sparql $@

../patterns/imports/seed_sorted.txt: ../patterns/imports/seed.txt
	cat ../patterns/imports/seed.txt | sort | uniq > $@

#../patterns/imports/%_terms.txt: ../patterns/imports/seed.txt
#	grep -i $(OBO)/$*_ $< > $@ || true  # Returns 1 if grep is empty

../patterns/imports/%_import.owl: mirror/%.owl ../patterns/imports/seed_sorted.txt
	$(ROBOT) extract -i $< -T ../patterns/imports/seed_sorted.txt --method BOT -O mirror/$*.owl annotate --ontology-iri $(OBO)/$(ONT)/patterns/imports/$*_import.owl -o $@

patterns: $(PATTERN_IMPORTS)

pattern_files := $(wildcard ../patterns/*.yaml)
pattern_tsv_files := $(wildcard ../patterns/*.tsv)

# TODO - move declarations like this to top
IMS=target/intermediates

$(IMS)/patterns/%.ofn: ../patterns/%.yaml ../patterns/%.tsv $(ONT)-edit.owl
	mkdir -p $(IMS)/patterns &&\
	dosdp-tools generate --catalog=catalog-v001.xml --infile=$(word 2, $^) --template=$< --ontology=$(word 3, $^) --obo-prefixes=true  --outfile=$@


pattern_modules := $(patsubst %.yaml, $(IMS)/patterns/%.ofn, $(notdir $(wildcard ../patterns/*.yaml)))

../patterns/definitions.owl: $(pattern_modules)
	$(ROBOT) merge $(addprefix -i , $(pattern_modules)) annotate --ontology-iri $(OBO)/$(ONT)/patterns/defintions.owl -o $@








