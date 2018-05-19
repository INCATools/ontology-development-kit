
# Building docker image
VERSION = "v0.0.2" 
IM=obolibrary/osklite

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name osklite $(IM)

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
