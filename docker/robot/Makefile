
# Building docker image
VERSION = "v1.2.0-alpha" 
IM=obolibrary/robot

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name robot $(IM)

clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made 

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

test: build
	docker images | grep oskfull &&\
	cd ../.. && make test CMD=./seed-via-docker.sh
