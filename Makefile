# import environment variables from docker-compose/.env file
ifneq (,$(wildcard docker-compose/.env))
  include docker-compose/.env
  export
endif

DOCKER_COMPOSE=docker-compose -f docker-compose/docker-compose.yaml

.PHONY: compose compose-down

# create external network for backend and bring up containers
compose:
	@echo "Checking for external network '$(BACKEND_NETWORK)'..."
	@if ! docker network ls | grep -q $(BACKEND_NETWORK); then \
	  echo "Creating external network: $(BACKEND_NETWORK)"; \
	  docker network create $(BACKEND_NETWORK); \
	else \
	  echo "External network '$(BACKEND_NETWORK)' already exists."; \
	fi
	@echo "Bringing up containers..."
	$(DOCKER_COMPOSE) up

# stop containers and remove external backend network
compose-down:
	@echo "Bringing down containers..."
	$(DOCKER_COMPOSE) down
	@echo "Removing external network '$(BACKEND_NETWORK)' if it exists..."
	@if docker network ls | grep -q $(BACKEND_NETWORK); then \
	  docker network rm $(BACKEND_NETWORK); \
	else \
	  echo "External network '$(BACKEND_NETWORK)' does not exist."; \
	fi

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