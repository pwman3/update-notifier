.PHONY: kustomization patche kustomize apply

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
print("\nVariable you can override: ")
print('\n'.join(variables))
endef

export PRINT_HELP_PYSCRIPT

PY ?= python3

APPNAME ?= $(shell basename $$(cd ..; pwd))
IMG ?= $(APPNAME)#? The image name to deploy

ORG ?= oz123#? Orgainization to push to
REGISTRY ?= registry.tiram.it#? container registry to push
TAG ?= $(shell git describe --always) ## Container tag

help:
	@$(PY) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

kustomization:: .SHELLFLAGS = -c eval
kustomization:: SHELL = bash -c 'eval "$${@//\\\\/}"'
kustomization::
	cat <<-EOF > kustomization.yml\
	apiVersion: kustomize.config.k8s.io/v1beta1\
	kind: Kustomization\
	namespace: $(APPNAME)\
	resources:\
	- deployment.yml\
	- service.yml\
	- limits.yml\
	- pvc.yml\
	- ingress.yml\
	images:\
	- name: registry/org/app:latest \
	  newName: localhost:32000/$(ORG)/$(APPNAME)\
	  newTag: v$(shell git describe --always)\
	patches:\
	- patchPVC.yml\
	- patchIngress.yml\
	- patchDeployment.yml\
	nameSuffix: -$(APPNAME)\
	commonLabels:\
	   app: $(APPNAME)\
	EOF

kustomize:: kustomization
	kubectl kustomize ./


apply::  ## apply a patched deployment
	kubectl apply -k ./

namespace::
	sed -e 's/%%NAME%%/'$(APPNAME)'/' ns-tmpl.yml | kubectl apply -f -
