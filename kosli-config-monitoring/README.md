


# Tracking kubernetes configmaps with kosli


1. download configmaps
2. filter out generated fields in configmaps
3. snapshot 


# Prerequisites

```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```


# Run all - download, filter and report to kosli
```bash
./all.sh
```


## 1. Download configmaps

```bash
gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1 --project test-kubernetes-environment

# Download Configmaps
./1-download-configmaps.sh -o snapdir gamestore

# Download CRDs
./1-download-configmaps.sh -o snapdir -c gamestore
```

## 2. Filter configmaps

```bash
source env/bin/activate

mkdir /tmp/snapdir
python src/filter_configmaps.py /tmp/snapdir

```


## 3. Snapshot downloaded configs

```bash
kosli snapshot server kubernetes-configurations \
  --paths "/tmp/snapdir/*"
```


# Running the tests

```bash
pytest
```