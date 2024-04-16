#!/bin/bash

set -e


# Report configmaps in the source directory to kosli as artifacts
# 
# Usage:
#
# ./attest-artifacts.sh 


GITHUB_SHA=$(git rev-parse HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
KOSLI_ORG=meekrosoft
KOSLI_FLOW=gamestore


kosli create flow --use-empty-template $KOSLI_FLOW --description "Tracking kubernetes config maps in Kosli"

kosli begin trail $GITHUB_SHA --flow $KOSLI_FLOW --description "Configmap changes in commit $GITHUB_SHA"


NS_DIR=config-sync-quickstart/multirepo/namespaces/gamestore
# for every file in NS_DIR
for file in $NS_DIR/*; do
    if [ -f "$file" ]; then
        echo "Processing $file"
		

		# get the filename from the path
		filename=$(basename $file)
		# replace / with . in the file path
		artifact=$(echo $file | sed 's/\//./g')
		#remove the file extension
		template_slot=$(echo $filename | sed 's/\..*//g')
		echo "Artifact: $artifact"
		echo "Filename: $filename"
		echo "Template Slot: $template_slot"

		# write this to a tmp file as json
		tmp_file=$(mktemp)
		yq -o=json eval 'sort_keys(..)' $file > "$tmp_file"

		kosli attest artifact $file \
			--artifact-type file \
			--build-url https://exampleci.com \
			--commit-url https://github.com/kosli-dev/k8s-config-management-with-kosli/commit/$GITHUB_SHA \
			--commit $GITHUB_SHA \
			--org $KOSLI_ORG \
			--flow $KOSLI_FLOW \
			--trail $GITHUB_SHA \
			--name $template_slot  

		kosli attest generic $file \
			--artifact-type file \
			--name configmap \
			--flow yourFlowName \
			--org $KOSLI_ORG \
			--flow $KOSLI_FLOW \
			--trail $GITHUB_SHA \
			--user-data $tmp_file \
			--attachments $file
		rm $tmp_file
	fi
done
