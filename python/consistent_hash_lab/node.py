"""
Node implementation for consistent hashing.

Defines the Node class with ID, optional replicas, and hash identifier.
"""
import hashlib
from typing import Optional


class Node:
    """
    A node in the consistent hash ring.
    
    Attributes:
        node_id: Unique identifier for the node
        replicas: Number of virtual nodes (vnodes) for this physical node
        weight: Weight of the node for weighted consistent hashing
    """
    
    def __init__(self, node_id: str, replicas: int = 1, weight: float = 1.0):
        """
        Initialize a new node.
        
        Args:
            node_id: Unique string identifier for the node
            replicas: Number of virtual replicas for this node
            weight: Weight for weighted hashing (higher weight = more keys)
        """
        self.node_id = node_id
        self.replicas = replicas
        self.weight = weight
    
    def get_hash_values(self, hash_function: str = "sha256") -> list[int]:
        """
        Generate hash values for this node and all its replicas.
        
        Args:
            hash_function: Hash function to use ("sha256" or "fnv1a")
            
        Returns:
            List of hash values for the node and its replicas
        """
        hash_values = []
        
        for replica in range(self.replicas):
            # Create unique identifier for each replica
            replica_id = f"{self.node_id}-{replica}"
            hash_value = self._hash_string(replica_id, hash_function)
            hash_values.append(hash_value)
        
        return hash_values
    
    def _hash_string(self, value: str, hash_function: str) -> int:
        """
        Hash a string using the specified hash function.
        
        Args:
            value: String to hash
            hash_function: Hash function to use
            
        Returns:
            Integer hash value
        """
        if hash_function == "sha256":
            return int(hashlib.sha256(value.encode()).hexdigest(), 16)
        elif hash_function == "fnv1a":
            # Simple FNV-1a implementation
            hash_value = 2166136261  # FNV offset basis
            for byte in value.encode():
                hash_value ^= byte
                hash_value *= 16777619  # FNV prime
                hash_value &= 0xFFFFFFFF  # Keep it 32-bit
            return hash_value
        else:
            raise ValueError(f"Unsupported hash function: {hash_function}")
    
    def __str__(self) -> str:
        """String representation of the node."""
        return f"Node({self.node_id}, replicas={self.replicas}, weight={self.weight})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the node."""
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """Check equality based on node_id."""
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
    
    def __hash__(self) -> int:
        """Hash function for using Node as dict key."""
        return hash(self.node_id)
