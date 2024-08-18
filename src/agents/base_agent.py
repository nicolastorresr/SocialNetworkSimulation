import uuid
from typing import Dict, List
import random

class BaseAgent:
    def __init__(self, personality: Dict[str, float], content_preferences: List[str]):
        self.id = uuid.uuid4()
        self.personality = personality
        self.content_preferences = content_preferences
        self.connections = set()
        self.messages = []

    def generate_message(self) -> str:
        topic = random.choice(self.content_preferences)
        sentiment = sum(self.personality.values()) / len(self.personality)
        return f"Message about {topic} with sentiment {sentiment:.2f} from {self.id}"

    def interact(self, message: str) -> bool:
        # Simple interaction logic based on content preference
        for preference in self.content_preferences:
            if preference in message:
                return random.random() < 0.7  # 70% chance to interact if preferred topic
        return random.random() < 0.3  # 30% chance to interact otherwise

    def update_connections(self, network):
        # Remove connections with low interaction
        to_remove = [conn for conn in self.connections if random.random() < 0.1]
        for conn in to_remove:
            self.connections.remove(conn)
            network.remove_connection(self.id, conn)

        # Add new connections
        potential_connections = set(network.agents.keys()) - self.connections - {self.id}
        new_connections = random.sample(potential_connections, min(3, len(potential_connections)))
        for conn in new_connections:
            self.connections.add(conn)
            network.add_connection(self.id, conn)
