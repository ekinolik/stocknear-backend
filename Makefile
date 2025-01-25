# packages this repo on a container
.PHONY: build-docker
build-docker:
	@docker build . -t stocknear:latest -f Dockerfile

# so you can access the bash on a container, for running manually or debugging
.PHONY: docker-bash
docker-bash:
	@docker run --rm -it --entrypoint bash  stocknear:latest

# run it
.PHONY: docker-run
docker-run:
	@docker run stocknear:latest
