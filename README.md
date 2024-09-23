# SocialNetworkSimulation
This project simulates a social network using autonomous agents based on Large Language Models (LLMs) to study the emergence of influencers and information spread patterns.

## Considerations

1. Having Python version greater than 3.9 and lower than 3.11.0

## Setup

1. Clone the repository:
```
git clone https://github.com/nicolastorresr/SocialNetworkSimulation.git
cd SocialNetworkSimulation
```
2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
3. Install the required packages:
```
pip install -r requirements.txt
```

## Running the Simulation

1. Configure the simulation parameters in `config/simulation_config.yaml`.

2. Run the simulation:
```
python scripts/run_simulation.py
```
4. Analyze the results:
```
python scripts/analyze_results.py
```

## Project Structure

- `src/`: Contains the main source code
- `agents/`: Defines agent behaviors and types
- `network/`: Implements the social network structure
- `simulation/`: Contains the main simulation logic
- `analysis/`: Includes scripts for analyzing results
- `config/`: Contains configuration files
- `data/`: Stores raw and processed data from simulations
- `notebooks/`: Jupyter notebooks for data exploration and visualization
- `tests/`: Unit tests for various components
- `scripts/`: Executable scripts for running simulations and analysis

## Running Tests

To run the unit tests:
```
python -m unittest discover tests
```
## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
