import unittest
import sys
import os
import tempfile

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from simulation.simulator import Simulator

class TestSimulator(unittest.TestCase):
    def setUp(self):
        # Create a temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_config.write("""
simulation:
  num_agents: 10
  duration: 10
agents:
  types:
    - name: "influencer"
      proportion: 0.2
    - name: "casual"
      proportion: 0.8
  personality_traits:
    - openness
    - conscientiousness
network:
  initial_connections_mean: 2
  initial_connections_std: 1
  connection_update_frequency: 5
content:
  topics:
    - politics
    - entertainment
    - technology
        """)
        self.temp_config.close()
        self.simulator = Simulator(self.temp_config.name)

    def tearDown(self):
        os.unlink(self.temp_config.name)

    def test_initialization(self):
        self.simulator.initialize()
        self.assertEqual(len(self.simulator.network.agents), 10)
        self.assertGreater(len(self.simulator.network.graph.edges()), 0)

    def test_run_simulation(self):
        self.simulator.initialize()
        self.simulator.run()
        # Check if messages were generated
        total_messages = sum(len(agent.messages) for agent in self.simulator.network.agents.values())
        self.assertGreater(total_messages, 0)

    def test_agent_types(self):
        self.simulator.initialize()
        influencers = sum(1 for agent in self.simulator.network.agents.values() if agent.__class__.__name__ == 'InfluencerAgent')
        self.assertGreater(influencers, 0)
        self.assertLess(influencers, 10)  # Not all agents should be influencers

    def test_network_updates(self):
        self.simulator.initialize()
        initial_edges = self.simulator.network.graph.number_of_edges()
        self.simulator.run()
        final_edges = self.simulator.network.graph.number_of_edges()
        self.assertNotEqual(initial_edges, final_edges)  # Network should have changed

if __name__ == '__main__':
    unittest.main()
