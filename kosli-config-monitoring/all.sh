#!/bin/bash

set -e

./1-download-configmaps.sh -o snapdir gamestore
./2-filter-configmaps.sh   
./3-snapshot-configmaps.sh
