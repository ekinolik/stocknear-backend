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

# bring up backend and external rependencies (e.g: redis)
.PHONY: compose
compose:
	@docker-compose -f docker-compose/docker-compose.yaml up

# stop containers
.PHONY: compose-down
compose-down:
	@docker-compose -f docker-compose/docker-compose.yaml down