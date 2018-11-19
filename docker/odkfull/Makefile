
# Building docker image
VERSION = "v1.1.6" 
IM=obolibrary/odkfull

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

run:
	docker run --rm -ti --name odkfull $(IM)

clean:
	docker kill $(IM) || echo not running ;
	docker rm $(IM) || echo not made 

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest

test: build
	docker images | grep oskfull &&\
	cd ../.. && make test CMD=./seed-via-docker.sh
