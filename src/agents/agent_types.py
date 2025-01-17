from .base_agent import BaseAgent
import random

class InfluencerAgent(BaseAgent):
    def __init__(self, personality, content_preferences, api_key):
        super().__init__(personality, content_preferences, api_key)
        self.influence_score = random.uniform(0.7, 1.0)

    def generate_message(self, context):
        base_message = super().generate_message(context)
        return f"Trending: {base_message}"

    def interact(self, message: str) -> bool:
        # Influencers are more likely to interact
        return super().interact(message) or random.random() < self.influence_score

class CasualAgent(BaseAgent):
    def __init__(self, personality, content_preferences, api_key):
        super().__init__(personality, content_preferences, api_key)
        self.activity_level = random.uniform(0.1, 0.5)

    def generate_message(self, context):
        if random.random() < self.activity_level:
            return super().generate_message(context)
        return None  # No message generated

    def interact(self, message: str) -> bool:
        # Casual agents are less likely to interact
        return super().interact(message) and random.random() < self.activity_level
