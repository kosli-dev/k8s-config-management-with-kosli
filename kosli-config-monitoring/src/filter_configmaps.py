import json
import yaml



def load_configmap(file_path):
    """Load a ConfigMap from a file"""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_configmap_json(file_path):
    """Load a ConfigMap from a file"""
    with open(file_path, "r") as f:
        return json.load(f)

def visit_leaf_nodes(configmap, ctx=[]):
        '''Visit all leaf nodes of a nested dictionary  
            Return a list containing the path to the leaf node and its value
        '''
        leaf_nodes = []
        for key, value in configmap.items():
            if isinstance(value, dict):
                # print("visiting dict", key, value)
                leaf_nodes.extend(visit_leaf_nodes(value, ctx + [key]))
            else:
                # print("visiting leaf", key, value)
                leaf_nodes.append(tuple(ctx + [key, value]))
        return leaf_nodes


def remove_items(initial_configmap, filter_list):
    """
    Remove items from the initial_configmap based on the filter_list
    """
    filter_items = visit_leaf_nodes(filter_list)

    # for every leaf node in the filter list, remove the corresponding key from the to_be_filtered
    for leaf_node in filter_items:
        # pop the last element from the leaf node
        leaf_node = leaf_node[:-1]
        print("removing", leaf_node)
        # remove the key from the deepcopy
        if(len(leaf_node) == 1):
            try:
                initial_configmap.pop(leaf_node[0], None)
            except KeyError as k:
                print("KeyError", k)
        elif(len(leaf_node) == 2):
            try:
                initial_configmap[leaf_node[0]].pop(leaf_node[1], None)
            except KeyError as k:
                print("KeyError", k)
        elif(len(leaf_node) == 3):
            try:
                initial_configmap[leaf_node[0]][leaf_node[1]].pop(leaf_node[2], None)
            except KeyError as k:
                print("KeyError", k)

        elif(len(leaf_node) == 4):
            try:
                initial_configmap[leaf_node[0]][leaf_node[1]][leaf_node[2]].pop(leaf_node[3], None)
            except KeyError as k:
                print("KeyError", k)
        elif(len(leaf_node) == 5):
            try:
                initial_configmap[leaf_node[0]][leaf_node[1]][leaf_node[2]][leaf_node[3]].pop(leaf_node[4], None)
            except KeyError as k:
                print("KeyError", k)
        else:
            print("Error: leaf node is too deep")
            assert False
 


# main
if __name__ == "__main__":

    # get the output directory from the command line argument
    import sys
    output_dir = sys.argv[1]

    # create a tmp dir
    import os
    import shutil
    import tempfile
    tmp_dir = output_dir
    print("tmp_dir:", tmp_dir)

    # for every file in snapdir, load the configmap and remove the items in filter_list
    snapdir = "snapdir"
    for file in os.listdir(snapdir):
        if file.endswith(".json"):
            print("processing", file)
            configmap = load_configmap(os.path.join(snapdir, file))
            filter_list = load_configmap("configsync-ignore-list.yaml")
            remove_items(configmap, filter_list)
            with open(os.path.join(tmp_dir, file), "w") as f:
                
                json.dump(configmap, f, indent=2)
                f.write("\n")
                #yaml.dump(configmap, f)


                