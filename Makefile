# This makefile is purely for running tests on the complete ontology-development-kit package on travis;
# users should not need to use this

# command used in make test.
# this can be changed to seed-via-docker.sh;
# but this should NOT be the default for environments like travis which
# run in a docker container anyway
CMD = ./odk/odk.py seed

EMAIL_ARGS=

CACHE=

ARCH=$(shell uname -m | sed 's/x86_64/amd64/')
PLATFORMS=linux/amd64,linux/arm64

.PHONY: .FORCE

custom_tests: test_no_yaml_dependencies_none test_no_yaml_dependencies_ro_pato test_no_yaml_dependencies_ro_pato_cl test_go_mini

test_no_yaml_dependencies_none:
	$(CMD) $(EMAIL_ARGS) -c -t my-ontology1 myont

test_no_yaml_dependencies_ro_pato:
	$(CMD) $(EMAIL_ARGS) -c -d pato -d ro -t my-ontology2 myont

test_no_yaml_dependencies_ro_pato_cl:
	$(CMD) $(EMAIL_ARGS) -c -d pato -d cl -d ro -t my-ontology3 myont

test_go_mini:
	$(CMD) -c -C examples/go-mini/project.yaml -s examples/go-mini/go-edit.obo -D target/go-mini

test_odklite_programs:
	@./tests/test-program.sh ROBOT robot --version
	@./tests/test-program.sh DOSDP-TOOLS dosdp-tools -v
	@./tests/test-program.sh OWLTOOLS owltools --version
	@./tests/test-program.sh AMMONITE sh amm --help

test_odkfull_programs: test_odklite_programs
	@./tests/test-program.sh KONCLUDE Konclude -h
	@./tests/test-program.sh SOUFFLE souffle --version
	@./tests/test-program.sh JENA jena
	@./tests/test-program.sh SPARQL sparql --version

test_odkdev_programs: test_odkfull_programs

TESTS = $(notdir $(wildcard tests/*.yaml))
TEST_FILES = $(foreach n,$(TESTS), tests/$(n))
#TEST_FILES = tests/test-release.yaml
test: $(TEST_FILES) custom_tests
	echo "All tests passed successfully!"

tests/*.yaml: .FORCE
	$(CMD) -c -C $@

schema/project-schema.json:
	./odk/odk.py dump-schema > $@

# Building docker image
VERSION = "v1.2.30"
IM=obolibrary/odkfull
IMLITE=obolibrary/odklite
DEV=obolibrary/odkdev
ROB=obolibrary/robot
#ROBOT_JAR="https://github.com/monarch-ebi-dev/odk_utils/raw/master/robot_maven_test.jar"
ROBOT_JAR_ARGS=#--build-arg ROBOT_JAR=$(ROBOT_JAR)

build: build-odklite
	docker build $(CACHE) --platform $(ARCH) \
	    --build-arg ODK_VERSION=$(VERSION) $(ROBOT_JAR_ARGS) \
	    -t $(IM):$(VERSION) -t $(IM):latest -t $(DEV):latest \
	    .

build-odklite: build-builder
	$(MAKE) -C docker/odklite ARCH=$(ARCH) CACHE=$(CACHE) \
		IM=$(IMLITE) VERSION=$(VERSION) build

build-builder:
	$(MAKE) -C docker/builder ARCH=$(ARCH) CACHE=$(CACHE) build

build-no-cache:
	$(MAKE) build CACHE=--no-cache

build-dev:
	docker build --build-arg ODK_VERSION=$(VERSION) --platform $(ARCH) \
	    -t $(DEV):$(VERSION) -t $(DEV):latest \
	    .

clean:
	docker kill $(IM) || echo not running
	docker rm $(IM) || echo not made


#### TESTING #####

test-flavor:
	@if docker images | grep -q odk$(FLAVOR) ; then \
		$(MAKE) test_odk$(FLAVOR)_programs IMAGE=odk$(FLAVOR) ; \
		$(MAKE) test CMD=./seed-via-docker.sh IMAGE=odk$(FLAVOR) ; \
	else \
		echo "Image obolibrary/odk$(FLAVOR) not locally available" ; \
	fi

test-full: build
	$(MAKE) test-flavor FLAVOR=full

test-dev: build-dev
	$(MAKE) test-flavor FLAVOR=dev

test-lite: build-odklite
	$(MAKE) test-flavor FLAVOR=lite

tests: test-full test-dev

test-no-build:
	$(MAKE) test-flavor FLAVOR=full

test-dev-no-build:
	$(MAKE) test-flavor FLAVOR=dev

test-lite-no-build:
	$(MAKE) test-flavor FLAVOR=lite


#### Publishing #####

publish-no-build:
	docker push $(DEV):$(VERSION)
	docker push $(DEV):latest
	docker push $(IM):latest
	docker push $(IM):$(VERSION)
	$(MAKE) -C docker/odklite publish-no-build

publish: build
	$(MAKE) publish-no-build

publish-dev-no-build:
	docker push $(DEV):$(VERSION)
	docker push $(DEV):latest

publish-multiarch:
	$(MAKE) -C docker/builder CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
		publish-multiarch
	$(MAKE) -C docker/odklite IM=$(IMLITE) VERSION=$(VERSION) \
	    CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
	    publish-multiarch
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
	    --build-arg ODK_VERSION=$(VERSION) \
	    -t $(IM):$(VERSION) -t $(IM):latest -t $(DEV):latest \
	    .

clean-tests:
	rm -rf target/*
