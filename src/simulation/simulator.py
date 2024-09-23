from network.social_network import SocialNetwork
from agents.agent_types import InfluencerAgent, CasualAgent
import random
import yaml

class Simulator:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.network = SocialNetwork()
        self.num_agents = self.config['simulation']['num_agents']
        self.duration = self.config['simulation']['duration']
        self.api_key = self.config['llm']['api_key']
        self.snapshots = [self.config['output']['save_network_snapshots'], self.config['output']['snapshot_frequency']]

    def initialize(self):
        for _ in range(self.num_agents):
            # personality = {trait: round(random.uniform(0.2, 1.0), 1) for trait in self.config['agents']['personality_traits']}
            personality = {trait: round(random.uniform(0.2, 1.0), 1) for trait in random.sample(self.config['agents']['personality_traits'], 5)}
            content_preferences = random.sample(self.config['content']['topics'], 3)
            if random.random() < self.config['agents']['types'][0]['proportion']:
                agent = InfluencerAgent(personality, content_preferences, self.api_key)
            else:
                agent = CasualAgent(personality, content_preferences, self.api_key)
            self.network.add_agent(agent)
            print(agent.id)

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
        for agent in self.network.agents.values():
            context = self._get_context(agent)
            message = agent.generate_message(context)
            if message:
                self.network.propagate_message(agent.id, message)


    def _get_context(self, agent):
        context = []
        for neighbor in self.network.get_neighbors(agent.id):
            context.extend(neighbor.messages[-2:])  # Get last 2 messages from each neighbor
        return context[-10:]  # Limit context to last 10 messages

    def update_network(self):
        for agent in self.network.agents.values():
            agent.update_connections(self.network)
