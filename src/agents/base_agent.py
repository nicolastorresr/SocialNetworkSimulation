import uuid
import random
import openai
from typing import Dict, List, Optional

class BaseAgent:
    def __init__(self, personality: Dict[str, float], content_preferences: List[str], api_key: str):
        self.id = str(uuid.uuid4())
        self.personality = personality
        self.content_preferences = content_preferences
        self.connections = set()
        self.messages = []
        openai.api_key = api_key

    def generate_message(self, context: List[str]) -> Optional[str]:
        prompt = self._create_message_prompt(context)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a social media user."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error generating message for agent {self.id}: {e}")
            return None

    def _create_message_prompt(self, context: List[str]) -> str:
        personality_str = ", ".join([f"{k}: {v:.2f}" for k, v in self.personality.items()])
        preferences_str = ", ".join(self.content_preferences)
        context_str = "\n".join(context[-5:])  # Use last 5 messages for context

        return f"""
        You are a social media user with the following personality traits:
        {personality_str}

        Your content preferences are: {preferences_str}

        Recent messages in your network:
        {context_str}

        Given your personality and preferences, and considering the recent messages, 
        generate a short social media post (max 280 characters):
        """

    def interact(self, message: str) -> bool:
        prompt = self._create_interaction_prompt(message)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a social media user."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1
            )
            return response.choices[0].message['content'].strip().lower() == "yes"
        except Exception as e:
            print(f"Error deciding interaction for agent {self.id}: {e}")
            return False

    def _create_interaction_prompt(self, message: str) -> str:
        personality_str = ", ".join([f"{k}: {v:.2f}" for k, v in self.personality.items()])
        preferences_str = ", ".join(self.content_preferences)

        return f"""
        You are a social media user with the following personality traits:
        {personality_str}

        Your content preferences are: {preferences_str}

        You've encountered the following message:
        "{message}"

        Based on your personality and preferences, would you interact with this message?
        Answer with only 'yes' or 'no':
        """

    def update_connections(self, network):
        # Remove connections with low interaction
        to_remove = [conn for conn in self.connections if random.random() < 0.1]
        # for agent in self.connections:
        #     print(agent)
        # print("jnbdYV6EW")
        for conn in to_remove:
            #self.connections.remove(conn)
            network.remove_connection(self.id, conn)

        # Add new connections
        potential_connections = set(network.agents.keys()) - self.connections - {self.id}
        new_connections = random.sample(potential_connections, min(3, len(potential_connections)))
        for conn in new_connections:
            self.connections.add(conn)
            network.add_connection(self.id, conn)
