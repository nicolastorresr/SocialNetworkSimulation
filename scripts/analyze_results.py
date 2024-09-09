import os
import sys
import json
import matplotlib.pyplot as plt
from collections import Counter

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from network.social_network import SocialNetwork
from agents.base_agent import BaseAgent
from agents.agent_types import InfluencerAgent, CasualAgent
from analysis.network_analysis import calculate_centrality, detect_communities, calculate_clustering_coefficient, visualize_network
from analysis.influencer_detection import identify_influencers, calculate_engagement_rate, analyze_influencer_trends
from analysis.message_analysis import analyze_sentiment, extract_topics, track_message_spread

def load_simulation_data(input_dir, api_key):
    network = SocialNetwork()

    # Load network structure
    with open(os.path.join(input_dir, 'network_structure.json'), 'r') as f:
        network_data = json.load(f)
    
    network.graph.add_nodes_from(network_data['nodes'])
    network.graph.add_edges_from(network_data['edges'])

    # Load agent data
    with open(os.path.join(input_dir, 'agent_data.json'), 'r') as f:
        agent_data = json.load(f)
    
    for agent_id, data in agent_data.items():
        if data['type'] == 'InfluencerAgent':
            agent = InfluencerAgent(data['personality'], data['content_preferences'], api_key)
        else:
            agent = CasualAgent(data['personality'], data['content_preferences'], api_key)
        
        agent.id = agent_id
        agent.connections = set(data['connections'])
        agent.messages = data['messages']
        network.agents[agent_id] = agent

    return network

def analyze_network(network, output_dir):
    print("Analyzing network...")
    
    # Calculate and save centrality
    centrality = calculate_centrality(network)
    with open(os.path.join(output_dir, 'centrality.json'), 'w') as f:
        json.dump({str(k): v for k, v in centrality.items()}, f)

    # Detect and save communities
    communities = detect_communities(network)
    with open(os.path.join(output_dir, 'communities.json'), 'w') as f:
        json.dump([list(c) for c in communities], f)

    # Calculate and save clustering coefficient
    clustering_coeff = calculate_clustering_coefficient(network)
    with open(os.path.join(output_dir, 'clustering_coefficient.txt'), 'w') as f:
        f.write(str(clustering_coeff))

    # Visualize network
    visualize_network(network)
    plt.savefig(os.path.join(output_dir, 'network_visualization.png'))

def analyze_influencers(network, output_dir):
    print("Analyzing influencers...")
    
    influencers = identify_influencers(network)
    with open(os.path.join(output_dir, 'influencers.json'), 'w') as f:
        json.dump({str(k): v for k, v in influencers.items()}, f)

    engagement_rates = {agent_id: calculate_engagement_rate(network, agent_id) for agent_id in influencers}
    with open(os.path.join(output_dir, 'engagement_rates.json'), 'w') as f:
        json.dump({str(k): v for k, v in engagement_rates.items()}, f)

    trends = analyze_influencer_trends(network, time_period=100)
    with open(os.path.join(output_dir, 'influencer_trends.json'), 'w') as f:
        json.dump(trends, f)

def analyze_messages(network, output_dir):
    print("Analyzing messages...")
    
    all_messages = [msg for agent in network.agents.values() for msg in agent.messages]
    
    # Analyze sentiment
    sentiments = [analyze_sentiment(msg) for msg in all_messages]
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments, bins=20)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'sentiment_distribution.png'))

    # Extract topics
    topics = extract_topics(all_messages)
    with open(os.path.join(output_dir, 'topics.txt'), 'w') as f:
        f.write('\n'.join(topics))

    # Track message spread (for the first message as an example)
    if all_messages:
        spread = track_message_spread(network, all_messages[0])
        plt.figure(figsize=(10, 6))
        plt.plot(list(spread.keys()), list(spread.values()))
        plt.title('Message Spread Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Number of Agents Reached')
        plt.savefig(os.path.join(output_dir, 'message_spread.png'))

def main():
    # Assume the latest simulation result is in the most recently created directory
    results_dir = 'data'
    simulation_dirs = [d for d in os.listdir(results_dir) if d.startswith('simulation_results_')]
    latest_simulation = max(simulation_dirs)
    input_dir = os.path.join(results_dir, latest_simulation)
    
    print(f"Loading simulation data from {input_dir}...")
    api_key = "ola"
    network = load_simulation_data(input_dir, api_key)
    
    output_dir = os.path.join(input_dir, 'analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    analyze_network(network, output_dir)
    analyze_influencers(network, output_dir)
    analyze_messages(network, output_dir)
    
    print(f"Analysis completed. Results saved in {output_dir}")

if __name__ == "__main__":
    main()
