
# Building docker image
VERSION = "v1.9.7"
IM=obolibrary/robot

CACHE=

ARCH=linux/$(shell uname -m | sed 's/x86_64/amd64/')
PLATFORMS=linux/amd64,linux/arm64

build:
	docker build $(CACHE) --platform $(ARCH) \
	    -t $(IM):$(VERSION) -t $(IM):latest \
	    .

build-no-cache:
	$(MAKE) build CACHE=--no-cache

clean:
	docker kill $(IM) || echo not running
	docker rm $(IM) || echo not made

publish-no-build:
	docker push $(IM):$(VERSION)
	docker push $(IM):latest

publish: build
	$(MAKE) publish-no-build

publish-multiarch:
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
	    -t $(IM):$(VERSION) -t $(IM):latest \
	    .
