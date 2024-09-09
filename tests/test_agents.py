import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from agents.base_agent import BaseAgent
from agents.agent_types import InfluencerAgent, CasualAgent
from network.social_network import SocialNetwork

class TestBaseAgent(unittest.TestCase):
    def setUp(self, api_key):
        self.agent = BaseAgent({'openness': 0.5, 'conscientiousness': 0.5}, ['technology', 'science'], api_key)

    def test_generate_message(self):
        message = self.agent.generate_message()
        self.assertIsInstance(message, str)
        self.assertTrue('technology' in message or 'science' in message)

    def test_interact(self):
        self.assertTrue(self.agent.interact("Interesting technology news!"))
        self.assertFalse(self.agent.interact("Unrelated topic"))

    def test_update_connections(self):
        network = SocialNetwork()
        other_agent = BaseAgent({}, [])
        network.add_agent(self.agent)
        network.add_agent(other_agent)
        network.add_connection(self.agent.id, other_agent.id)
        
        initial_connections = len(self.agent.connections)
        self.agent.update_connections(network)
        self.assertNotEqual(initial_connections, len(self.agent.connections))

class TestInfluencerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = InfluencerAgent({'openness': 0.8, 'conscientiousness': 0.8}, ['politics', 'entertainment'])

    def test_generate_message(self):
        message = self.agent.generate_message()
        self.assertIsInstance(message, str)
        self.assertTrue(message.startswith("Trending:"))

    def test_interact(self):
        # Influencers are more likely to interact
        interactions = [self.agent.interact("Random message") for _ in range(100)]
        self.assertTrue(sum(interactions) > 50)  # Should interact more than 50% of the time

class TestCasualAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CasualAgent({'openness': 0.3, 'conscientiousness': 0.3}, ['sports', 'music'])

    def test_generate_message(self):
        messages = [self.agent.generate_message() for _ in range(100)]
        self.assertTrue(any(message is None for message in messages))  # Should sometimes not generate a message
        self.assertTrue(any(message is not None for message in messages))  # Should sometimes generate a message

    def test_interact(self):
        # Casual agents are less likely to interact
        interactions = [self.agent.interact("Random message") for _ in range(100)]
        self.assertTrue(sum(interactions) < 50)  # Should interact less than 50% of the time

if __name__ == '__main__':
    unittest.main()
