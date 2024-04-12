#!/bin/bash

set -e


# Report configmaps in the source directory to kosli as artifacts
# 
# Usage:
#
# ./attest-artifacts.sh 


GIT_COMMIT=$(git rev-parse HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

kosli create flow --use-empty-template $KOSLI_FLOW --description "Tracking kubernetes config maps in Kosli"

kosli begin trail $GITHUB_SHA --flow $KOSLI_FLOW


kosli attest artifact FILE.tgz \
	--artifact-type file \
	--build-url https://exampleci.com \
	--commit-url https://github.com/kosli-dev/k8s-config-management-with-kosli/commit/$GITHUB_SHA \
	--commit $GITHUB_SHA \
	--flow $KOSLI_FLOW \
	--trail $GITHUB_SHA \
	--name yourTemplateArtifactName \
	--api-token yourApiToken \
	--org yourOrgName