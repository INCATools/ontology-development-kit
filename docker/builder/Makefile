CACHE=

ARCH=linux/$(shell uname -m | sed 's/x86_64/amd64/')
PLATFORMS=linux/amd64,linux/arm64

build:
	docker build $(CACHE) --platform $(ARCH) -f Dockerfile \
	    -t obolibrary/odkbuild:latest \
	    ../..

build-no-cache:
	$(MAKE) build CACHE=--no-cache

publish-multiarch:
	docker buildx build $(CACHE) --platform $(PLATFORMS) -f Dockerfile \
		-t obolibrary/odkbuild:latest --push \
		../..
