import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from network.social_network import SocialNetwork
from agents.base_agent import BaseAgent

class TestSocialNetwork(unittest.TestCase):
    def setUp(self):
        self.network = SocialNetwork()
        self.agent1 = BaseAgent({}, [])
        self.agent2 = BaseAgent({}, [])
        self.network.add_agent(self.agent1)
        self.network.add_agent(self.agent2)

    def test_add_agent(self):
        self.assertIn(self.agent1.id, self.network.agents)
        self.assertIn(self.agent1.id, self.network.graph.nodes())

    def test_add_connection(self):
        self.network.add_connection(self.agent1.id, self.agent2.id)
        self.assertIn(self.agent2.id, self.network.graph.neighbors(self.agent1.id))
        self.assertIn(self.agent2.id, self.agent1.connections)

    def test_remove_connection(self):
        self.network.add_connection(self.agent1.id, self.agent2.id)
        self.network.remove_connection(self.agent1.id, self.agent2.id)
        self.assertNotIn(self.agent2.id, self.network.graph.neighbors(self.agent1.id))
        self.assertNotIn(self.agent2.id, self.agent1.connections)

    def test_get_neighbors(self):
        self.network.add_connection(self.agent1.id, self.agent2.id)
        neighbors = self.network.get_neighbors(self.agent1.id)
        self.assertIn(self.agent2, neighbors)

    def test_propagate_message(self):
        self.network.add_connection(self.agent1.id, self.agent2.id)
        message = "Test message"
        self.network.propagate_message(self.agent1.id, message)
        self.assertIn(message, self.agent2.messages)

if __name__ == '__main__':
    unittest.main()
