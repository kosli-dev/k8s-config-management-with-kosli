import pytest
from src import filter_configmaps, load_configmap, visit_leaf_nodes, remove_items

def test_load_configmap():
    configmap = load_configmap("./test/original-configmap.yaml")
    assert configmap["apiVersion"] == "v1"
    assert configmap["kind"] == "ConfigMap"
    assert configmap["metadata"]["name"] == "store-inventory"


def test_load_configmap_wrong_file():
    with pytest.raises(FileNotFoundError):
        load_configmap("wrong-file.yaml")


def test_visit_leaf_nodes_empty():
    initial_configmap = {}
    expected_leaf_nodes = []
    assert visit_leaf_nodes(initial_configmap) == expected_leaf_nodes


def test_visit_leaf_nodes():
    initial_configmap = {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "marketplace.com/comments": "What about chess?"
            },
        },
        "data": {
            "competitive": "300",
        }
    }

    expected_leaf_nodes = [
        ("apiVersion", "v1"),
        ("metadata", "name", "store-inventory"),
        ("metadata", "annotations", "marketplace.com/comments", "What about chess?"),
        ("data", "competitive", "300"),
    ]

    leaf_nodes = visit_leaf_nodes(initial_configmap)
    assert leaf_nodes == expected_leaf_nodes

    
def test_remove_items_in_configmap_that_are_in_filter_list():
    initial_configmap = {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "marketplace.com/comments": "What about chess?",
                "blah": "blah"
            },
        },
        "data": {
            "competitive": "300",
        }
    }
    
    filter_list = {
        "metadata": {
            "annotations": {
                "marketplace.com/comments": None
            },
        },
    }

    remove_items(initial_configmap, filter_list)

    assert initial_configmap == {
        "apiVersion": "v1",
        "metadata": {
            "name": "store-inventory",
            "annotations": {
                "blah": "blah"
            },
        },
        "data": {
            "competitive": "300",
        }
    }




def test_filter_configmap():
    downloaded_configmap = load_configmap("./test/downloaded-configmap.yaml")
    ignore_list = load_configmap("configsync-ignore-list.yaml")
    remove_items(downloaded_configmap, ignore_list)
    assert downloaded_configmap == {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "store-inventory",
            "namespace": "gamestore",
            "annotations": {
                "marketplace.com/comments": "What about chess?"
            },
            "labels": {},
        },
        "data": {
            "single_player": "20",
            "cooperative": "60",
            "competitive": "300",
        },   
    }



if __name__ == "__main__":
    pytest.main()