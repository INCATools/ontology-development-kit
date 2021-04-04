
# Building docker image
VERSION = "v1.2.27" 
IM=obolibrary/odklite

build:
	@docker build -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

docker-build-no-cache:
	@docker build  --build-arg ODK_VERSION=$(VERSION) --no-cache -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest
	
docker-build:
	@docker build --build-arg ODK_VERSION=$(VERSION) -t $(IM):$(VERSION) . \
	&& docker tag $(IM):$(VERSION) $(IM):latest

publish: build
	@docker push $(IM):$(VERSION) \
	&& docker push $(IM):latest
