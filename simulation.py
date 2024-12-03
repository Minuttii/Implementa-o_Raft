import time
from raft_node import RaftNode
from raft_cluster import RaftCluster

def main():
    cluster = RaftCluster()

    
    for i in range(5):
        node = RaftNode(node_id=i, cluster=cluster)
        cluster.add_node(node)

    cluster.start_all()

   
    time.sleep(5)
    cluster.fail_node(2)
    time.sleep(5)
    cluster.recover_node(2)
    time.sleep(10)

    
    print("Finalizando simulação.")
    for node in cluster.nodes.values():
        node.active = False

if __name__ == "__main__":
    main()
