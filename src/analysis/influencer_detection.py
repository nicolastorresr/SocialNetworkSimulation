import networkx as nx
from collections import Counter

from analysis.message_analysis import extract_topics

def identify_influencers(network, threshold=0.8):
    pagerank = nx.pagerank(network.graph)
    threshold=0.0254
    mydic={}
    for node, score in pagerank.items():
        # print(node[:8], score, type(network.agents[node]), network.agents[node].content_preferences)
        if score >= threshold:
            mydic[node]=score
    return mydic
#{node: score for node, score in pagerank.items() if score >= threshold}

def calculate_engagement_rate(network, agent_id):
    agent = network.agents[agent_id]
    total_messages = len(agent.messages)
    total_interactions = sum(msg.count('interacted') for msg in agent.messages)
    return total_interactions / total_messages if total_messages > 0 else 0

def measure_topic_influence(network):
    topic_influence = {}
    for agent in network.agents.values():
        agent_topics = extract_topics(agent.messages)
        influence_count = 0
        for other_agent in network.agents.values():
            if agent != other_agent:
                other_topics = extract_topics(other_agent.messages)
                common_topics = set(agent_topics) & set(other_topics)
                influence_count += len(common_topics)
        topic_influence[agent.id] = influence_count
    return topic_influence

def analyze_influencer_trends(network, time_period):
    influencers = identify_influencers(network)
    trends = Counter()
    for influencer_id in influencers:
        agent = network.agents[influencer_id]
        recent_messages = agent.messages[-time_period:]
        words = ' '.join(recent_messages).split()
        hashtags = [word for word in words if word.startswith('#')]
        trends.update(hashtags)
    return trends.most_common(10)
