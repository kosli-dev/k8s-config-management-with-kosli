#!/bin/bash

set -e

# Usage:
# ./2-snapshot-configmaps.sh 
#
# 

kosli snapshot server kubernetes-configurations \
  --paths "/tmp/snapdir/*"