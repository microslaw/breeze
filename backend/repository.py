import os
import pickle

def write_pickle(object, path):
    with open(path, 'wb') as f:
        pickle.dump(object, f)

def read_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_all_node_instances():
    nodes_dir = "./backend/data/nodes"
    return [
        node_id.split("_")[1].strip(".pickle")
        for node_id in os.listdir(nodes_dir)
    ]

def get_node_instance(node_id):
    nodes_dir = "./backend/data/nodes"
    try:
        return read_pickle(f"{nodes_dir}/node_{node_id}.pickle")
    except FileNotFoundError:
        return "Node not found", 404
