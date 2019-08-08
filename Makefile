# This makefile is purely for running tests on the complete ontology-development-kit package on travis;
# users should not need to use this

# command used in make test.
# this can be changed to seed-via-docker.sh;
# but this should NOT be the default for environments like travis which
# run in a docker container anyway
CMD = ./odk/odk.py seed

EMAIL_ARGS=

test: test1 test2 test3 test4 test-go-mini test-patterns test-release1 test-release2 test-release3 test-github-release

test1:
	$(CMD) $(EMAIL_ARGS) -c -d pato -t my-ontology1 myont

test2:
	$(CMD) $(EMAIL_ARGS) -c -d pato -d ro -t my-ontology2 myont

test3:
	$(CMD) $(EMAIL_ARGS) -c -d pato -d cl -d ro -t my-ontology3 myont

test4:
	$(CMD) -c -C examples/triffo/project.yaml

test-go-mini:
	$(CMD) -c -C examples/go-mini/project.yaml -s examples/go-mini/go-edit.obo -D target/go-mini

test-patterns:
	$(CMD) -c -C examples/pattern-test/project.yaml

test-release1:
	$(CMD) -c -C examples/release-artefacts-test/test-release-format-patterns.yaml
	
test-release2:
	$(CMD) -c -C examples/release-artefacts-test/test-release-format.yaml

test-release3:
	$(CMD) -c -C examples/release-artefacts-test/test-release.yaml
	
test-github-release:
	$(CMD) -c -C examples/tests/test-github-release.yaml

schema/project-schema.json:
	./odk/odk.py dump-schema > $@

# Building docker image
VERSION = "v1.2.17" 
IM=obolibrary/odkfull
DEV=obolibrary/odkdev

docker-build:
	@docker build  --build-arg ODK_VERSION=$(VERSION) --no-cache -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest
	
docker-build-use-cache:
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
	
docker-publish: docker-build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

docker-test: docker-build-use-cache
	docker images | grep odkfull &&\
	make test CMD=./seed-via-docker.sh
	
docker-test-no-build:
	docker images | grep odkfull &&\
	make test CMD=./seed-via-docker.sh

docker-publish-all: docker-publish
	(cd docker/osklite && make publish VERSION=$(VERSION))

