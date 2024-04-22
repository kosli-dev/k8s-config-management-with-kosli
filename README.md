# Tracking K8S configmaps with Kosli

This is a demo repo to show how to track kubernetes configmaps in Kosli, where the configmaps are synced with google config sync.

You can find the demo config maps [here](/config-sync-quickstart/multirepo/namespaces/gamestore/)


### 1. Report configmap changes with Github Actions and Kosli Flows

When a change to the source repo occurs, the [main action](/.github/workflows/main.yaml) runs to report the configmaps to kosli.  To get a reproducible result, we "compile" the yaml to a sorted json format in the [attest-artifacts.sh](/attest-artifacts.sh) script.

An improvement would be to add an option to only report configmaps that change in the git commit.

### 2. Monitoring the configmaps

A [second Github Action](/.github/workflows/monitor.yaml) is defined to record the configmaps in the kubernetes cluster.  This runs manually, but can also be set up to run on a schedule.  You can view the readme for the proces [here](/kosli-config-monitoring/README.md).
