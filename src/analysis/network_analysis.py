import networkx as nx
import matplotlib.pyplot as plt

def calculate_centrality(network):
    return nx.pagerank(network.graph)

def detect_communities(network):
    return nx.community.louvain_communities(network.graph.to_undirected())

def calculate_clustering_coefficient(network):
    return nx.average_clustering(network.graph)

def visualize_network(network):
    pos = nx.spring_layout(network.graph)
    plt.figure(figsize=(12, 8))
    nx.draw(network.graph, pos, node_color='lightblue', with_labels=False, node_size=30)
    plt.title("Social Network Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('network_visualization.png')
    plt.close()
