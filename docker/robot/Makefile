
# Building docker image
VERSION = "v1.8.1" 
IM=obolibrary/robot

docker-build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made 

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
