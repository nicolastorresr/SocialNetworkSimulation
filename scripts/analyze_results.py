import os
import sys
import json
import yaml
import openai
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from collections import Counter

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from network.social_network import SocialNetwork
from agents.base_agent import BaseAgent
from agents.agent_types import InfluencerAgent, CasualAgent
from analysis.network_analysis import calculate_centrality, detect_communities, calculate_clustering_coefficient, visualize_network
from analysis.influencer_detection import identify_influencers, calculate_engagement_rate, measure_topic_influence, analyze_influencer_trends
from analysis.message_analysis import analyze_sentiment, extract_topics, track_message_spread

def load_simulation_data(input_dir, api_key, sufix=""):
    network = SocialNetwork()

    config_path = 'config/sim_config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    network.pool_personality = config["agents"]["personality_traits"]
    network.pool_preference = config["content"]["topics"]

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

def analyze_network(network, output_dir, sufix=""):
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

def analyze_influencers(network, output_dir, sufix=""):
    print("Analyzing influencers...")
    influencers = identify_influencers(network)
    with open(os.path.join(output_dir, 'influencers.json'), 'w') as f:
        json.dump({str(k): v for k, v in influencers.items()}, f)

    engagement_rates = {agent_id: calculate_engagement_rate(network, agent_id) for agent_id in influencers}
    with open(os.path.join(output_dir, 'engagement_rates.json'), 'w') as f:
        json.dump({str(k): v for k, v in engagement_rates.items()}, f)
    
    # topic_influence = measure_topic_influence(network)
    # with open(os.path.join(output_dir, 'topic_influence.json'), 'w') as f:
    #     json.dump({str(k): v for k, v in topic_influence.items()}, f)

    trends = analyze_influencer_trends(network, time_period=100)
    with open(os.path.join(output_dir, 'influencer_trends.json'), 'w') as f:
        json.dump(trends, f)

def analyze_messages(network, output_dir, sufix=""):
    print("Analyzing messages...")

    all_messages = [msg for agent in network.agents.values() for msg in agent.messages]

    # Analyze sentiment
    sentiments = [analyze_sentiment(msg) for msg in all_messages]

    # Analyze sentiment polarization
    positive_count = sum(1 for s in sentiments if s > 0)
    neutral_count = sum(1 for s in sentiments if s == 0)
    negative_count = sum(1 for s in sentiments if s < 0)

    # Extract topics
    topics = extract_topics(all_messages)
    with open(os.path.join(output_dir, 'topics.txt'), 'w') as f:
        f.write('\n'.join(topics))

    # Track message spread
    if all_messages:
        spread = track_message_spread(network, all_messages[0])

    # Analyze message counts per agent
    message_counts = [len(agent.messages) for agent in network.agents.values()]
    agent_ids = list(network.agents.keys())

    message_data = {
        'sentiments': sentiments,
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'topics': topics,
        'spread': spread,
        'message_counts': dict(zip(agent_ids, message_counts))
    }
    
    with open(os.path.join(output_dir, 'message_data.json'), 'w') as json_file:
        json.dump(message_data, json_file, indent=4)

    print(f"Results saved to {output_dir}")

def network_evolution(network, output_dir):
    agent_evolution = {}
    for agent in network.agents:
        context = network.agents[agent].messages
        print(agent)
        prompt = agent_evolution_prompt(network.pool_personality, network.pool_preference, context)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt}
                ],
                max_tokens=200
            )
            agent_evolution[agent] = {
                "detected_traits_and_preferences": response.choices[0].message['content'].strip()
            }
        except Exception as e:
            print(f"Error generating personality analysis for agent {agent}: {e}")
            return None
        
        topics = response.choices[0].message['content'].strip().split("\n")
        personalities = topics[0]
        print(topics)
        topics = topics[1]
        personalities = personalities.split(",")
        topics = topics.split(",")

        grade_t = 0
        grade_p = 0

        for topic in topics:
            if topic.strip() in network.agents[agent].content_preferences:
                grade_t +=1
        
        for personality in personalities:
            if personality.strip() in network.agents[agent].personality:
                grade_p +=1
        
        
        agent_evolution[agent]["grade_t"] = 3 - grade_t
        agent_evolution[agent]["grade_p"] = 5 - grade_p

    with open(os.path.join(output_dir, 'agent_evolution.json'), 'w') as json_file:
        json.dump(agent_evolution, json_file, indent=4)

def agent_evolution_prompt(pool_personality, pool_preference, context):
    context_str = "\n".join(context[-5:])  # Use last 5 messages for context

    return f"""
    You are a personality and content preference analyzer. Based on the following list of possible personality traits and content preferences, 
    analyze the recent messages and infer the most relevant traits and preferences.

    Possible personality traits: {pool_personality}
    Possible content preferences: {pool_preference}

    Recent messages:
    {context_str}

    Based on this information, ONLY AND EXCLUSIVELY GENERATE TWO LISTS. The first list correspond to 5 personalities traits and the second list corresponds to 3 content preferences that best match the sender's behavior. The format is: 
    element1, element2, ... , element5
    element1, element2,  element3
    """

def main():
    # Assume the latest simulation result is in the most recently created directory
    results_dir = 'data'
    simulation_dirs = [d for d in os.listdir(results_dir) if d.startswith('simulation_results_')]
    latest_simulation = max(simulation_dirs)
    input_dir = os.path.join(results_dir, latest_simulation)
    print(f"Loading simulation data from {input_dir}...")
    api_key = "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"
    output_dir = os.path.join(input_dir, 'analysis')
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isdir(input_dir+"/snapshots"):
        print("Loading simulation data from "+input_dir+"/snapshots...")
        iteraciones = 0
        flag = False
        for carpeta_raiz, subcarpetas, archivos in os.walk(input_dir+"/snapshots"):
            if flag:
                network = load_simulation_data(carpeta_raiz, api_key)
                sufix_actual = carpeta_raiz.strip().split("/")[-1]
                os.makedirs(output_dir+"/"+sufix_actual, exist_ok=True)
                analyze_network(network, output_dir+"/"+sufix_actual)
                analyze_influencers(network, output_dir+"/"+sufix_actual)
                analyze_messages(network, output_dir+"/"+sufix_actual)

            flag = True

    network = load_simulation_data(input_dir, api_key)
    analyze_network(network, output_dir)
    analyze_influencers(network, output_dir)
    analyze_messages(network, output_dir)

    openai.api_key = api_key
    network_evolution(network,output_dir)

    print(f"Analysis completed. Results saved in {output_dir}")
    
if __name__ == "__main__":
    main()
