
# Building docker image
VERSION = "v1.1.6" 
IM=obolibrary/odklite

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name odklite $(IM)

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
