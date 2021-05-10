# This makefile is purely for running tests on the complete ontology-development-kit package on travis;
# users should not need to use this

# command used in make test.
# this can be changed to seed-via-docker.sh;
# but this should NOT be the default for environments like travis which
# run in a docker container anyway
CMD = ./odk/odk.py seed

EMAIL_ARGS=

CACHE=

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
VERSION = "v1.2.28"
IM=obolibrary/odkfull
IMLITE=obolibrary/odklite
DEV=obolibrary/odkdev
ROB=obolibrary/robot
#ROBOT_JAR="https://github.com/monarch-ebi-dev/odk_utils/raw/master/robot_maven_test.jar"
ROBOT_JAR_ARGS=#--build-arg ROBOT_JAR=$(ROBOT_JAR)

build:
	docker build $(CACHE) \
	    --build-arg ODK_VERSION=$(VERSION) $(ROBOT_JAR_ARGS) \
	    -t $(IM):$(VERSION) -t $(IM):latest -t $(DEV):latest \
	    .
	$(MAKE) -C docker/odklite IM=$(IMLITE) VERSION=$(VERSION) CACHE=$(CACHE) build
	$(MAKE) -C docker/robot CACHE=$(CACHE) build

build-no-cache:
	$(MAKE) build CACHE=--no-cache

build-dev:
	docker build --build-arg ODK_VERSION=$(VERSION) \
	    -t $(DEV):$(VERSION) -t $(DEV):latest \
	    .

clean:
	docker kill $(IM) || echo not running
	docker rm $(IM) || echo not made


#### TESTING #####

test-flavor:
	docker images | grep odk$(FLAVOR) && \
	    $(MAKE) test CMD=./seed-via-docker.sh

test-full: build
	$(MAKE) test-flavor FLAVOR=full

test-dev: build-dev
	$(MAKE) test-flavor FLAVOR=dev

test-lite: build
	$(MAKE) test-flavor FLAVOR=lite

test: test-full test-dev

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
	$(MAKE) -C docker/robot publish-no-build

publish: build
	$(MAKE) publish-no-build

publish-dev-no-build:
	docker push $(DEV):$(VERSION)
	docker push $(DEV):latest

publish-multiarch:
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
	    --build-arg ODK_VERSION=$(VERSION) \
	    -t $(IM):$(VERSION) -t $(IM):latest -t $(DEV):latest \
	    .
	$(MAKE) -C docker/odklite IM=$(IMLITE) VERSION=$(VERSION) \
	    CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
	    publish-multiarch
	$(MAKE) -C docker/robot CACHE=$(CACHE) PLATFORMS=$(PLATFORMS) \
	    publish-multiarch

clean-tests:
	rm -rf target/*
