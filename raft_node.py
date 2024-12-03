import threading
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class RaftNode:
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

    def __init__(self, node_id, cluster):
        self.node_id = node_id
        self.cluster = cluster
        self.state = self.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.lock = threading.Lock()
        self.active = True  

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        while self.active:
            if self.state == self.FOLLOWER:
                self.follower_loop()
            elif self.state == self.CANDIDATE:
                self.candidate_loop()
            elif self.state == self.LEADER:
                self.leader_loop()
            time.sleep(0.1)

    def follower_loop(self):
        timeout = random.uniform(3, 5)
        start_time = time.time()
        while time.time() - start_time < timeout and self.active:
            if self.state != self.FOLLOWER:
                return
            time.sleep(0.1)
        self.start_election()

    def candidate_loop(self):
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1
        logging.info(f"Node {self.node_id} started election for term {self.current_term}")
        for peer in self.cluster.get_peers(self.node_id):
            if peer.request_vote(self.node_id, self.current_term):
                votes += 1
        if votes > len(self.cluster.nodes) // 2:
            self.state = self.LEADER
            logging.info(f"Node {self.node_id} became leader for term {self.current_term}")
        else:
            self.state = self.FOLLOWER

    def leader_loop(self):
        while self.state == self.LEADER and self.active:
            for peer in self.cluster.get_peers(self.node_id):
                peer.append_entries(self.node_id, self.current_term, [])
            logging.info(f"Node {self.node_id} (Leader) sent heartbeat")
            time.sleep(1)

    def request_vote(self, candidate_id, term):
        with self.lock:
            if term > self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
                self.voted_for = candidate_id
                self.current_term = term
                logging.info(f"Node {self.node_id} voted for Node {candidate_id} in term {term}")
                return True
        return False

    def append_entries(self, leader_id, term, entries):
        with self.lock:
            if term >= self.current_term:
                self.current_term = term
                self.state = self.FOLLOWER
                logging.info(f"Node {self.node_id} accepted entries from Leader {leader_id}")
                return True
        return False

    def fail(self):
        self.active = False
        logging.warning(f"Node {self.node_id} has failed.")

    def recover(self):
        self.active = True
        logging.warning(f"Node {self.node_id} has recovered.")
        self.start_election()
