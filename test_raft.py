import unittest
from raft_node import RaftNode
from raft_cluster import RaftCluster

class TestRaftConsensus(unittest.TestCase):

    def setUp(self):
        
        self.cluster = RaftCluster()
        for i in range(5):
            node = RaftNode(node_id=i, cluster=self.cluster)
            self.cluster.add_node(node)
        self.cluster.start_all()

    def tearDown(self):
        
        for node in self.cluster.nodes.values():
            node.active = False

    def test_leader_election(self):
        
        leaders = [node for node in self.cluster.nodes.values() if node.state == RaftNode.LEADER]
        self.assertEqual(len(leaders), 1, "Deve haver exatamente um líder no cluster.")

    def test_fail_and_recover_node(self):
        
        self.cluster.fail_node(2)
        failed_node = self.cluster.nodes[2]
        self.assertFalse(failed_node.active, "O nó 2 deve estar inativo após falha.")

        self.cluster.recover_node(2)
        self.assertTrue(failed_node.active, "O nó 2 deve estar ativo após recuperação.")
        self.assertEqual(failed_node.state, RaftNode.FOLLOWER, "O nó recuperado deve estar no estado de seguidor.")

    def test_consensus_with_failures(self):
        
        self.cluster.fail_node(3)
        time.sleep(3)  
        leaders = [node for node in self.cluster.nodes.values() if node.state == RaftNode.LEADER]
        self.assertEqual(len(leaders), 1, "O cluster deve alcançar consenso com apenas um líder, mesmo com falhas.")
