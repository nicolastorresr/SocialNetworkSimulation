import os
import sys
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from simulation.simulator import Simulator

def save_simulation_data(network, output_dir,iter="", folder=""):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir+folder, exist_ok=True)
    os.makedirs(output_dir+folder+iter, exist_ok=True)

    # Save network structure
    network_data = {
        'nodes': list(network.graph.nodes()),
        'edges': list(network.graph.edges())
    }
    with open(os.path.join(output_dir+folder+iter, 'network_structure.json'), 'w') as f:
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
    with open(os.path.join(output_dir+folder+iter, 'agent_data.json'), 'w') as f:
        json.dump(agent_data, f)

def running(sim, output_dir):
    print("Running simulation...")
    if sim.save_initial_network_state:
        save_simulation_data(sim.network, output_dir,folder="/initial/")

    for step in range(sim.duration):
        print("Step: "+str(step))
        sim.run()

        if step % sim.config['network']['connection_update_frequency'] == 0:
            sim.update_network()

        if step % sim.config['network']['agent_invitation_frequency'] == 0:
            sim.invite_agent()

        if (step % sim.snapshot_frequency == 0) and (sim.save_network_snapshots):
            # each snapshots is saved on a folder named by its iteration
            save_simulation_data(sim.network, output_dir, str(step),"/snapshots/") 
    print("Simulation completed.")
    

def main():
    config_path = 'config/sim_config.yaml'
    sim = Simulator(config_path)
    
    print("Initializing simulation...")
    sim.initialize()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f'data/simulation_results_{timestamp}'

    # Run simulations
    running(sim, output_dir)
    # Save final simulation state
    save_simulation_data(sim.network, output_dir, "")
    
    print(f"Simulation data saved in {output_dir}")

if __name__ == "__main__":
    main()