
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

all: sparql_test all_imports $(ONT).owl $(ONT).obo ../patterns/pattern.owl ../patterns/definitions.owl
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
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_import.obo,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

# Add '--check false' flag if your OWL is not obo-strict
imports/%_import.obo: imports/%_import.owl
	$(ROBOT) convert -i $< -o $@

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

#  run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	robot verify -i $< --queries $(VQUERIES) -O reports/

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


PATTERN_IMPORT_ONTOLOGIES = MY_IMPORTS_LIST 

PATTERN_IMPORTS = pattern.owl seed.txt $(patsubst %, imports/%_terms.txt,$(IMPORTS)) $(patsubst %, imports/%_import.owl,$(PATTERN_IMPORT_ONTOLOGIES))



# Better to make this an intermediate & merge with pattern.owl file having correct iri and import statements - configured by make

../patterns/pattern.owl: pattern_schema_checks
	$(DOSDPT) prototype --prefixes=../prefixes.yaml --template=. --outfile=$@

pattern_schema_checks:
	simple_pattern_tester.py ../patterns # 2>&1 | tee $@

../patterns/imports/seed.txt: ../patterns/pattern.owl
	$(ROBOT) query -f csv -i $< --query ../sparql/terms.sparql $@

../patterns/imports/%_terms.txt: ../patterns/imports/seed.txt
	grep -i $(OBO)/$*_ $< > $@

../patterns/imports/%_import.owl: mirror/%.owl ../patterns/imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@

pattern_imports: $(PATTERN_IMPORTS)

pattern_files := $(wildcard ../patterns/*.yaml)
pattern_tsv_files := $(wildcard ../patterns/*.tsv)

# TODO - move declarations like this to top
IMS=target/intermediates

$(IMS)/patterns/%.ofn: src/patterns/%.yaml src/patterns/%.tsv target/$(ONT)-edit-imports.ofn $(ONT_DIR)/$(ONT)-edit.ofn
	mkdir -p $(IMS)/patterns &&\
	dosdp-tools generate --catalog=$(UTIL)/catalog-v001.xml --infile=$(word 2, $^) --template=$< --ontology=$(ONT_DIR)/$(ONT)-edit.ofn --obo-prefixes=true --outfile=$@

# This is broken!
pattern_modules := $(patsubst %.yaml, $(IMS)/patterns/%.ofn, $(notdir $(wildcard ../patterns/*.yaml)))

test_ps:
	echo $(pattern_modules)

../patterns/definitions.owl: $(pattern_modules)
	$(ROBOT) merge $(addprefix -i , $(pattern_modules)) annotate --ontology-iri $(PREFIX)/$(ONT)-patterns.ofn -o $@

###  Now extend to roll individual definitions files from 
###  See ultimate MakeFile for way of doing this

# ../patterns/defintions.owl: ../patterns/definitions.owl
#	$(DOSDPT) generate ../patterns/util/prefixes.yaml --output $@ # DOSDP-tools command TBA or set of DOSDP-tools commands?  Latter requires make to find all filenames




