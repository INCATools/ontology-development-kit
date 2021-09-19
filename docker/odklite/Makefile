
# Building docker image
VERSION = "v1.2.30"
IM=obolibrary/odklite

CACHE=

PLATFORMS=linux/amd64,linux/arm64

build:
	docker build $(CACHE) -f Dockerfile \
	    --build-arg ODK_VERSION=$(VERSION) \
	    -t $(IM):$(VERSION) -t $(IM):latest \
	    ../..

build-no-cache:
	$(MAKE) build CACHE=--no-cache

publish-no-build:
	docker push $(IM):$(VERSION)
	docker push $(IM):latest

publish: build
	$(MAKE) publish-no-build

publish-multiarch:
	docker buildx build $(CACHE) --push --platform $(PLATFORMS) \
	    --build-arg ODK_VERSION=$(VERSION) \
	    -t $(IM):$(VERSION) -t $(IM):latest \
	    ../..
