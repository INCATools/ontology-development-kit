# This makefile is purely for running tests on the complete ontology-development-kit package on travis;
# users should not need to use this

# command used in make test.
# this can be changed to seed-via-docker.sh;
# but this should NOT be the default for environments like travis which
# run in a docker container anyway
CMD = ./odk/odk.py seed

EMAIL_ARGS=

CACHE=

ARCH=linux/$(shell uname -m | sed 's/x86_64/amd64/')
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
	@./tests/test-program.sh OORT ontology-release-runner --help
	@./tests/test-program.sh JINJANATOR jinjanate --version
	@./tests/test-program.sh DICER-CLI dicer-cli --version
	@./tests/test-program.sh SSSOM-CLI sssom-cli --version
	@./tests/test-program.sh ODK odk.py

test_odkfull_programs: test_odklite_programs
	@./tests/test-program.sh KONCLUDE Konclude -h
	@./tests/test-program.sh SOUFFLE souffle --version
	@./tests/test-program.sh JENA jena
	@./tests/test-program.sh OWLTOOLS owltools --version
	@./tests/test-program.sh AMMONITE sh amm --help
	@./tests/test-program.sh SCALA-CLI scala-cli --version
	@./tests/test-program.sh SPARQL sparql --version
	@./tests/test-program.sh SPARQLPROG pl2sparql -g halt
	@./tests/test-program.sh OBO-DASHBOARD obodash --help
	@./tests/test-program.sh RELATION-GRAPH relation-graph --version
	@./tests/test-program.sh OAKLIB runoak --help
	@./tests/test-program.sh SSSOM-PY sssom --version

test_odkdev_programs: test_odkfull_programs

TESTS = $(notdir $(wildcard tests/*.yaml))
TEST_FILES = $(foreach n,$(TESTS), tests/$(n))
#TEST_FILES = tests/test-release.yaml
test: $(TEST_FILES) custom_tests
	echo "All tests passed successfully!"

tests/*.yaml: .FORCE
	$(CMD) -c -C $@


.PHONY: docs
docs:
	@ODK_IMAGE=odklite ./odk.sh ./odk/odk.py dump-schema > schema/project-schema.json
	@ODK_IMAGE=odklite ./odk.sh python ./odk/schema_documentation.py

# Building docker image
VERSION = "v1.6"
IM=obolibrary/odkfull
IMLITE=obolibrary/odklite
ROB=obolibrary/robot
#ROBOT_JAR="https://github.com/monarch-ebi-dev/odk_utils/raw/master/robot_maven_test.jar"
ROBOT_JAR_ARGS=#--build-arg ROBOT_JAR=$(ROBOT_JAR)
TAGS_OPTION=-t $(IM):$(VERSION) -t $(IM):latest

build: build-odklite
	docker build $(CACHE) --platform $(ARCH) \
	    --build-arg ODK_VERSION=$(VERSION) $(ROBOT_JAR_ARGS) \
	    $(TAGS_OPTION) \
	    .

build-odklite: build-builder
	$(MAKE) -C docker/odklite ARCH=$(ARCH) CACHE=$(CACHE) \
		IM=$(IMLITE) VERSION=$(VERSION) build

build-robot:
	$(MAKE) -C docker/robot ARCH=$(ARCH) CACHE=$(CACHE) build

build-builder:
	$(MAKE) -C docker/builder ARCH=$(ARCH) CACHE=$(CACHE) build

build-no-cache:
	$(MAKE) build CACHE=--no-cache

build-odklite-dev: build-builder
	$(MAKE) TAGS_OPTION="-t $(IMLITE):dev" VERSION=$(VERSION)-dev build-odklite

build-dev: build-odklite-dev
	docker build $(CACHE) --platform $(ARCH) \
		--build-arg ODK_VERSION=$(VERSION)-dev \
		--build-arg ODKLITE_TAG=dev \
		$(ROBOT_JAR_ARGS) \
		-t $(IM):dev \
		.

clean:
	docker kill $(IM) || echo not running
	docker rm $(IM) || echo not made


#### TESTING #####

test-flavor:
	@if docker images | grep -q odk$(FLAVOR) ; then \
		$(MAKE) test_odk$(FLAVOR)_programs ODK_IMAGE=odk$(FLAVOR) ; \
		$(MAKE) test CMD=./seed-via-docker.sh ODK_IMAGE=odk$(FLAVOR) ; \
	else \
		echo "Image obolibrary/odk$(FLAVOR) not locally available" ; \
	fi

test-full: build
	$(MAKE) test-flavor FLAVOR=full

test-lite: build-odklite
	$(MAKE) test-flavor FLAVOR=lite

tests: test-full
	make test_odkfull_programs

test-no-build:
	$(MAKE) test-flavor FLAVOR=full

test-lite-no-build:
	$(MAKE) test-flavor FLAVOR=lite


#### Publishing #####

publish-no-build:
	docker push $(DEV):$(VERSION)
	docker push $(IM):latest
	docker push $(IM):$(VERSION)
	$(MAKE) -C docker/odklite publish-no-build

publish: build
	$(MAKE) publish-no-build

publish-multiarch:
	$(MAKE) -C docker/robot CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
		publish-multiarch
	$(MAKE) -C docker/builder CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
		publish-multiarch
	$(MAKE) -C docker/odklite IM=$(IMLITE) VERSION=$(VERSION) \
	    CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
	    publish-multiarch
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
	    --build-arg ODK_VERSION=$(VERSION) \
	    $(TAGS_OPTION) \
	    .

publish-multiarch-dev:
	$(MAKE) -C docker/builder CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
		publish-multiarch
	$(MAKE) -C docker/odklite IM=$(IMLITE) VERSION=$(VERSION)-dev \
		CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
		TAGS_OPTION="-t $(IMLITE):dev" \
		publish-multiarch
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
		--build-arg ODK_VERSION=$(VERSION)-dev \
		--build-arg ODKLITE_TAG=dev \
		-t $(IM):dev \
		.

# This should use the same base image as the one used to build the ODK itself.
constraints.txt: requirements.txt.full
	docker run -v $$PWD:/work -w /work --rm -ti ubuntu:24.04 /work/update-constraints.sh --in-docker

clean-tests:
	rm -rf target/*

dev-test-publish:
	git pull
	docker buildx rm multiarch
	docker buildx create --name multiarch --driver docker-container --use
	$(MAKE) tests publish-multiarch-dev

dev-test-publish-no-rm:
	git pull
	docker buildx create --name multiarch --driver docker-container --use
	$(MAKE) tests publish-multiarch-dev
