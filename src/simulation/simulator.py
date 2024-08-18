from src.network.social_network import SocialNetwork
from src.agents.agent_types import InfluencerAgent, CasualAgent
import random
import yaml

class Simulator:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.network = SocialNetwork()
        self.num_agents = self.config['simulation']['num_agents']
        self.duration = self.config['simulation']['duration']

    def initialize(self):
        for _ in range(self.num_agents):
            personality = {trait: random.random() for trait in self.config['agents']['personality_traits']}
            content_preferences = random.sample(self.config['content']['topics'], 3)
            if random.random() < self.config['agents']['types'][0]['proportion']:
                agent = InfluencerAgent(personality, content_preferences)
            else:
                agent = CasualAgent(personality, content_preferences)
            self.network.add_agent(agent)

        # Initialize connections
        for agent in self.network.agents.values():
            num_connections = int(random.gauss(
                self.config['network']['initial_connections_mean'],
                self.config['network']['initial_connections_std']
            ))
            potential_connections = set(self.network.agents.keys()) - {agent.id}
            for _ in range(num_connections):
                if potential_connections:
                    other_id = random.choice(list(potential_connections))
                    self.network.add_connection(agent.id, other_id)
                    potential_connections.remove(other_id)

    def run(self):
        for step in range(self.duration):
            for agent in self.network.agents.values():
                message = agent.generate_message()
                if message:
                    self.network.propagate_message(agent.id, message)
            if step % self.config['network']['connection_update_frequency'] == 0:
                self.update_network()

    def update_network(self):
        for agent in self.network.agents.values():
            agent.update_connections(self.network)
