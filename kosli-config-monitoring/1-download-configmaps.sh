#!/bin/bash

set -e

# Usage:
# ./download-configmaps.sh [-o <snapdir>]  [-c <ConfigMap|crdtype..>] <namespaceA,namespaceB> 
#
# Takes a list of namespaces to download configmaps/crds from as an arguemnt
# writes configmaps to the output directory with the namespace.configmapname as the filename
# output-dir is the directory to write the configmaps to - default is snapdir if not provided



output_dir=snapdir
crd_type=ConfigMap


# use getops to parse the arguments 
while getopts ":o:c:" opt; do
    case ${opt} in
        o )
            output_dir=$OPTARG
            ;;
        c )
            crd_type=$OPTARG
            ;;
        \? )
            echo "Usage: cmd [-o output_dir] [-c crd_type] namespace1,namespace2"
            ;;
    esac
done

echo Output directory: $output_dir
echo CRD Type: $crd_type

# Shift off the options and optional arguments
shift $((OPTIND -1))

# Now, "$@" contains the additional arguments
namespaces="$@"
# Check if the namespace argument is provided
if [ $# -ne 1 ]; then
    echo "Please provide a list of namespaces as an argument."
    exit 1
fi

echo "Namespaces: $namespaces"

mkdir -p $output_dir

#for each namespace, download the configmaps
for namespace in $(echo $namespaces | tr "," "\n")
do
    echo "Downloading $crd_type's for namespace: $namespace"
    if [ -z "$(kubectl get namespace $namespace -o name)" ]; then
        echo "Namespace '$namespace' does not exist."
        exit 1
    fi

    # for each namespace, download the configmaps
    configmaps=$(kubectl get $crd_type -n $namespace -o go-template='{{range .items}}{{.metadata.name}}{{printf "\n"}}{{end}}')  
    
    for configmap in $configmaps
    do
        configmap_json_filename=$output_dir/$namespace.$configmap.json
        echo Writing: $configmap_json_filename
        kubectl get $crd_type -n $namespace -o json $configmap > $configmap_json_filename

        # sort the keys in the yaml file
        tmp_file=$(mktemp)
        mv $configmap_json_filename $tmp_file
        jq -S . $tmp_file > $configmap_json_filename
    done
done

