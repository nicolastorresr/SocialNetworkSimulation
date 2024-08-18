import networkx as nx
from collections import Counter

def identify_influencers(network, threshold=0.8):
    pagerank = nx.pagerank(network.graph)
    return {node: score for node, score in pagerank.items() if score > threshold}

def calculate_engagement_rate(network, agent_id):
    agent = network.agents[agent_id]
    total_messages = len(agent.messages)
    total_interactions = sum(msg.count('interacted') for msg in agent.messages)
    return total_interactions / total_messages if total_messages > 0 else 0

def analyze_influencer_trends(network, time_period):
    influencers = identify_influencers(network)
    trends = Counter()
    for influencer_id in influencers:
        agent = network.agents[influencer_id]
        recent_messages = agent.messages[-time_period:]
        words = ' '.join(recent_messages).split()
        trends.update(words)
    return trends.most_common(10)
