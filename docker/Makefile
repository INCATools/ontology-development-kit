VERSION = "v0.0.1" 
IM=cmungall/osk

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name $(IM) osk

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
