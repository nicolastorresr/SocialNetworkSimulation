import random
import networkx as nx
from typing import List
from agents.base_agent import BaseAgent

class SocialNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.agents = {}

    def add_agent(self, agent: BaseAgent):
        self.graph.add_node(agent.id)
        self.agents[agent.id] = agent

    def add_connection(self, agent1_id, agent2_id):
        self.graph.add_edge(agent1_id, agent2_id)
        self.agents[agent1_id].connections.add(agent2_id)

    def remove_connection(self, agent1_id, agent2_id):
        self.graph.remove_edge(agent1_id, agent2_id)
        self.agents[agent1_id].connections.remove(agent2_id)

    def get_neighbors(self, agent_id) -> List[BaseAgent]:
        return [self.agents[n] for n in self.graph.neighbors(agent_id)]

    def propagate_message(self, sender_id, message):
        for neighbor_id in self.graph.neighbors(sender_id):
            if self.agents[neighbor_id].interact(message):
                self.agents[neighbor_id].messages.append(message)
