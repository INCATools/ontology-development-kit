# This makefile is purely for running tests on the complete ontology-starter-kit package on travis;
# users should not need to use this

test: test1 test2

test1:
	 ./seed-my-ontology-repo.pl -c -d pato -t my-ontology1 myont

test2:
	 ./seed-my-ontology-repo.pl -c -d pato -d ro -t my-ontology2 myont

test3:
	 ./seed-my-ontology-repo.pl -c -d pato -d cl -d ro -t my-ontology3 myont

# Building docker image
VERSION = "v0.0.1" 
IM=obolibrary/osk

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name $(IM) osk

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
