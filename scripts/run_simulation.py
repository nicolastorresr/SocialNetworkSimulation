import os
import sys
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from simulation.simulator import Simulator

def save_simulation_data(network, output_dir, sufix, folder=""):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir+folder, exist_ok=True)

    # Save network structure
    network_data = {
        'nodes': list(network.graph.nodes()),
        'edges': list(network.graph.edges())
    }
    with open(os.path.join(output_dir+folder, 'network_structure_'+sufix+'.json'), 'w') as f:
        json.dump(network_data, f)

    # Save agent data
    agent_data = {
        str(agent.id): {
            'type': agent.__class__.__name__,
            'personality': agent.personality,
            'content_preferences': agent.content_preferences,
            'connections': list(agent.connections),
            'messages': agent.messages
        } for agent in network.agents.values()
    }
    with open(os.path.join(output_dir+folder, 'agent_data_'+sufix+'.json'), 'w') as f:
        json.dump(agent_data, f)

def main():
    config_path = 'config/sim_config.yaml'
    sim = Simulator(config_path)
    
    print("Initializing simulation...")
    sim.initialize()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f'data/simulation_results_{timestamp}'

    save_simulation_data(sim.network, output_dir, "init")
    
    print("Running simulation...")
    for step in range(sim.duration):
        print(step)
        sim.run()

        if step % sim.config['network']['connection_update_frequency'] == 0:
            sim.update_network()

        if (step % sim.snapshots[1] == 0) and (sim.snapshots[0]):
            save_simulation_data(sim.network, output_dir, str(step),"/snapshots/")
    
    print("Simulation completed.")
    
    # Save simulation results
    save_simulation_data(sim.network, output_dir, "final")
    
    print(f"Simulation data saved in {output_dir}")

if __name__ == "__main__":
    main()