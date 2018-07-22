
# Building docker image
VERSION = "v0.0.4" 
IM=obolibrary/oskfull

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name oskfull $(IM)

clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made 

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
