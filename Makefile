.PHONY: docker-build docker-push docker-run run test

PY ?= python3

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

targets = []
variables = []

print("Targets:\n")
for line in sys.stdin:
    match = re.search(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        targets.append("%-20s %s" % (target, help))

    vars = re.search(r'([A-Z_]+).*#\? (.*)$$', line)
    if vars:
        target, help = vars.groups()
        variables.append("%-20s %s" % (target, help))

print('\n'.join(targets))
if variables:
    print("\nVariable you can override: ")
    print('\n'.join(variables))
endef

export PRINT_HELP_PYSCRIPT

run:## run the application
	python3 app.py


test: ## run a rudimentary test
	python3 test.py

help:
	@$(PY) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

REGISTRY ?= registry.tiram.it#? container registry to push
ORG ?= oz123#? organization to push to
IMG ?= pwman-notifier#? image name
TAG ?= $(shell git describe --always)#? tag name
OPTS ?=

# usage: make docker-build TAG=0.1
docker-build::  ## build a docker image
	docker build $(OPTS) -t $(REGISTRY)/$(ORG)/$(IMG):$(TAG) -f docker/Dockerfile .

docker-push::
	docker push $(REGISTRY)/$(ORG)/$(IMG):$(TAG)

docker-run::  ## run the docker image locally
	sudo chown -vR 33:33 $(CURDIR)/data/
	sudo docker run -it -p 9001:9001 -v $(CURDIR)/data:/var/lib/app/db:rw $(REGISTRY)/$(ORG)/$(IMG):$(TAG)
