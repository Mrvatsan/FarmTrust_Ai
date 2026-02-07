import numpy as np
import json

class FederatedLearningNode:
    """
    Edge AI Micro-Farm Network Node.
    Implements a simplified Federated Averaging (FedAvg) logic for 
    privacy-preserving model updates across regional farm devices.
    """
    def __init__(self, node_id, region):
        self.node_id = node_id
        self.region = region
        self.local_weights = None # Simulated model weights
        print(f"Federated Node '{node_id}' initialized in region '{region}'.")

    def train_locally(self, local_data_quality):
        """
        Simulates local training on regional produce variants.
        """
        # Generate dummy weights representing the local model state
        self.local_weights = np.random.randn(10) * local_data_quality
        print(f"Node {self.node_id} trained locally on {self.region} produce.")
        return self.local_weights

    def prepare_update(self):
        """
        Prepares a privacy-preserving update (gradient/weights) for the central server.
        """
        if self.local_weights is None:
            return None
        # In a real scenario, we might add differential privacy noise here
        return self.local_weights.tolist()

class FederatedLearningCentral:
    """
    Central Server for the Micro-Farm Network.
    Aggregates updates from various farm nodes.
    """
    def __init__(self):
        self.global_weights = np.zeros(10)
        self.node_count = 0
        print("Federated Central Aggregator Initialized.")

    def aggregate_updates(self, updates):
        """
        Implements FedAvg: Average the weights from all contributing nodes.
        """
        if not updates:
            return
            
        update_array = np.array(updates)
        self.global_weights = np.mean(update_array, axis=0)
        self.node_count = len(updates)
        print(f"Aggregated updates from {self.node_count} nodes. Global model updated.")
        return self.global_weights.tolist()

if __name__ == "__main__":
    # Simulation
    central = FederatedLearningCentral()
    
    node1 = FederatedLearningNode("Farm_A", "South_Asia")
    node2 = FederatedLearningNode("Farm_B", "Europe")
    
    update1 = node1.train_locally(0.8)
    update2 = node2.train_locally(0.9)
    
    new_global_weights = central.aggregate_updates([update1, update2])
    print(f"New Global Weights: {new_global_weights}")
