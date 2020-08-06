# This makefile is purely for running tests on the complete ontology-development-kit package on travis;
# users should not need to use this

# command used in make test.
# this can be changed to seed-via-docker.sh;
# but this should NOT be the default for environments like travis which
# run in a docker container anyway
CMD = ./odk/odk.py seed

EMAIL_ARGS=

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
test: custom_tests $(TEST_FILES)
	echo "All tests passed successfully!"
	
tests/*.yaml: .FORCE
	$(CMD) -c -C $@

schema/project-schema.json:
	./odk/odk.py dump-schema > $@

# Building docker image
VERSION = "v1.2.23"
IM=obolibrary/odkfull
DEV=obolibrary/odkdev

docker-build-no-cache:
	@docker build  --build-arg ODK_VERSION=$(VERSION) --no-cache -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest
	
docker-build:
	@docker build --build-arg ODK_VERSION=$(VERSION) -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest
	
docker-build-use-cache-dev:
	@docker build --build-arg ODK_VERSION=$(VERSION) -t $(DEV):$(VERSION) . \
	&& docker tag $(DEV):$(VERSION) $(DEV):latest

docker-run:
	docker run --rm -ti --name odkfull $(IM)

docker-clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made 

docker-publish-no-build:
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
	
docker-publish-dev-no-build:
	@docker push $(DEV):$(VERSION) \
	&& docker push $(DEV):latest
	
docker-publish: docker-build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

docker-test: docker-build
	docker images | grep odkfull &&\
	make test CMD=./seed-via-docker.sh

docker-test-no-build:
	docker images | grep odkfull &&\
	make test CMD=./seed-via-docker.sh
	
docker-test-dev-no-build:
	docker images | grep odkdev &&\
	make test CMD=./seed-via-docker.sh

docker-publish-all: docker-publish
	(cd docker/osklite && make publish VERSION=$(VERSION))

clean-tests:
	rm -rf target/*
