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
TARGET=target
IMPORTS = MY_IMPORTS_LIST


# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: patterns all_imports sparql_test $(ONT).owl $(ONT).obo
	echo 'Release files created successfully.'
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
	$(ROBOT)  reason -i $< -r ELK -e none relax reduce -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@ &&\
	echo "$(ONT).owl successfully created."

$(ONT).obo: $(ONT).owl
	$(ROBOT) convert --check false -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@ &&\
	echo "$(ONT).obo successfully created."

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

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
mirror/%.owl:
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


	# TODO - move declarations like this to top
	IMS=$(TARGET)/intermediates

	#PATTERN_IMPORTS = ../patterns/pattern.owl $(patsubst %, ../patterns/imports/%_import.owl,$(IMPORTS))


	# Better to make this an intermediate & merge with pattern.owl file having correct iri and import statements - configured by make


	# ----------------------------------------
	# Main command to generate the pattern ontology and the definitions
	# ----------------------------------------
	# The pattern.owl ontology contains the OWL versions of all the patterns currently in the patterns directory
	DOSDP_TEMP=$(IMS)/dosdp
	DOSDP_TEMP_PATTERN=$(DOSDP_TEMP)/patterns
	DOSDP_TEMP_PATTERN_MANUAL=$(DOSDP_TEMP_PATTERN)/manual
	DOSDP_TEMP_PATTERN_AUTO=$(DOSDP_TEMP_PATTERN)/auto
	DOSDP_TEMP_TERMS=$(DOSDP_TEMP)/terms
	DOSDP_TEMP_ONTOLOGIES=$(DOSDP_TEMP)/ontologies

	patterns: ../patterns/pattern.owl ../patterns/definitions.owl

	pattern_clean:
		rm -r $(DOSDP_TEMP)

	$(DOSDP_TEMP):
		mkdir -p $@

	$(DOSDP_TEMP_PATTERN):
		mkdir -p $@

	$(DOSDP_TEMP_TERMS):
		mkdir -p $@

	$(DOSDP_TEMP_ONTOLOGIES):
		mkdir -p $@

	$(DOSDP_TEMP_PATTERN_MANUAL): $(DOSDP_TEMP_PATTERN)
		mkdir -p $@

	$(DOSDP_TEMP_PATTERN_AUTO): $(DOSDP_TEMP_PATTERN)
		mkdir -p $@

	# ----------------------------------------
	# Build pattern.owl
	# ----------------------------------------
	# The pattern.owl ontology contains the OWL versions of all the patterns currently in the patterns directory

	../patterns/pattern.owl: pattern_schema_checks
		$(DOSDPT) prototype --obo-prefixes --template=../patterns/dosdp-patterns --outfile=$@

	pattern_schema_checks:
		simple_pattern_tester.py ../patterns/dosdp-patterns/ # 2>&1 | tee $@

	# ----------------------------------------
	# Build definitions.owl
	# ----------------------------------------
	# The following target will create a merged version of all imports indicated as project import dependencies (including the edit file itself), and then extract a module based
	# on the entities used in the TSV files
	individual_patterns_manual := $(patsubst %.tsv, $(DOSDP_TEMP_PATTERN_MANUAL)/%.ofn, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))
	individual_patterns_auto := $(patsubst %.tsv, $(DOSDP_TEMP_PATTERN_AUTO)/%.ofn, $(notdir $(wildcard ../patterns/data/auto/*.tsv)))
	pattern_term_lists_auto := $(patsubst %.tsv, $(DOSDP_TEMP_PATTERN_AUTO)/%.txt, $(notdir $(wildcard ../patterns/data/auto/*.tsv)))
	pattern_term_lists_manual := $(patsubst %.tsv, $(DOSDP_TEMP_PATTERN_MANUAL)/%.txt, $(notdir $(wildcard ../patterns/data/manual/*.tsv)))

	../patterns/definitions.owl: $(DOSDP_TEMP_PATTERN_MANUAL) $(individual_patterns_manual) $(individual_patterns_auto)
		$(ROBOT) merge $(addprefix -i , $(individual_patterns_manual)) $(addprefix -i , $(individual_patterns_auto)) annotate --ontology-iri $(OBO)/$(ONT)/patterns/definitions.owl -o $@

	$(DOSDP_TEMP_PATTERN_MANUAL)/%.ofn: ../patterns/data/manual/%.tsv ../patterns/dosdp-patterns/%.yaml $(DOSDP_TEMP_ONTOLOGIES)/all_imports_module.owl $(DOSDP_TEMP_PATTERN_MANUAL)
		dosdp-tools generate --infile=$< --template=$(word 2, $^) --ontology=$(word 3, $^) --obo-prefixes=true  --outfile=$@

	$(DOSDP_TEMP_PATTERN_AUTO)/%.ofn: ../patterns/data/auto/%.tsv ../patterns/dosdp-patterns/%.yaml $(DOSDP_TEMP_ONTOLOGIES)/all_imports_module.owl $(DOSDP_TEMP_PATTERN_AUTO)
		dosdp-tools generate --infile=$< --template=$(word 2, $^) --ontology=$(word 3, $^) --obo-prefixes=true  --outfile=$@

	$(DOSDP_TEMP_ONTOLOGIES)/all_imports_module.owl: $(DOSDP_TEMP_ONTOLOGIES)/all_pattern_terms.txt $(DOSDP_TEMP_ONTOLOGIES)/all_imports.owl $(DOSDP_TEMP_ONTOLOGIES)
		$(ROBOT) extract -i $(word 2, $^) -T $< --method BOT -o $@

	$(DOSDP_TEMP_ONTOLOGIES)/all_pattern_terms.txt: $(pattern_term_lists_auto) $(pattern_term_lists_manual) $(DOSDP_TEMP_ONTOLOGIES)
		cat $^ $(word 2, $^) | sort | uniq >$@

	$(DOSDP_TEMP_PATTERN_MANUAL)/%.txt: ../patterns/dosdp-patterns/%.yaml ../patterns/data/manual/%.tsv $(DOSDP_TEMP_PATTERN_MANUAL)
		dosdp-tools terms --infile=$(word 2, $^) --template=$< --obo-prefixes=true --outfile=$@

	$(DOSDP_TEMP_PATTERN_AUTO)/%.txt: ../patterns/dosdp-patterns/%.yaml ../patterns/data/auto/%.tsv $(DOSDP_TEMP_PATTERN_AUTO)
		dosdp-tools terms --infile=$(word 2, $^) --template=$< --obo-prefixes=true --outfile=$@

	imports_all_pattern := $(patsubst %, mirror/%.owl,$(IMPORTS))

	$(DOSDP_TEMP_ONTOLOGIES)/all_imports.owl: $(imports_all_pattern)
		echo 'imports: '$(imports_all_pattern) &&\
		$(ROBOT) merge $(addprefix -i , $^) annotate --ontology-iri $(DOSDP_TEMP_ONTOLOGIES)/all_imports.owl -o $@
