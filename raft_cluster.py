import random

class RaftCluster:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def get_peers(self, node_id):
        return [node for node in self.nodes.values() if node.node_id != node_id]

    def fail_node(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id].fail()

    def recover_node(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id].recover()

    def start_all(self):
        for node in self.nodes.values():
            node.start()
