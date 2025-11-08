"""
Consistent hash ring implementation.

Implements the core consistent hashing algorithm with support for adding/removing nodes
and finding the appropriate node for a given key.
"""
import bisect
import hashlib
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

try:
    from .node import Node
except ImportError:
    from node import Node


class ConsistentHashRing:
    """
    Implementation of a consistent hash ring.
    
    The ring maintains a sorted list of hash values and their corresponding nodes.
    Keys are mapped to nodes by finding the first node clockwise from the key's hash.
    """
    
    def __init__(self, hash_function: str = "sha256"):
        """
        Initialize an empty consistent hash ring.
        
        Args:
            hash_function: Hash function to use ("sha256" or "fnv1a")
        """
        self.hash_function = hash_function
        self.ring: List[Tuple[int, Node]] = []  # Sorted list of (hash_value, node)
        self.nodes: Dict[str, Node] = {}  # Map of node_id to Node
        self.hash_to_node: Dict[int, Node] = {}  # Map of hash_value to Node
    
    def add_node(self, node: Node) -> None:
        """
        Add a node to the hash ring.
        
        Args:
            node: Node to add to the ring
        """
        if node.node_id in self.nodes:
            raise ValueError(f"Node {node.node_id} already exists in the ring")
        
        self.nodes[node.node_id] = node
        
        # Get all hash values for this node (including replicas)
        hash_values = node.get_hash_values(self.hash_function)
        
        # Add each hash value to the ring
        for hash_value in hash_values:
            self.hash_to_node[hash_value] = node
            # Insert in sorted order
            bisect.insort(self.ring, (hash_value, node))
    
    def remove_node(self, node_id: str) -> Optional[Node]:
        """
        Remove a node from the hash ring.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            The removed node, or None if not found
        """
        if node_id not in self.nodes:
            return None
        
        node = self.nodes[node_id]
        hash_values = node.get_hash_values(self.hash_function)
        
        # Remove all hash values for this node
        for hash_value in hash_values:
            if hash_value in self.hash_to_node:
                del self.hash_to_node[hash_value]
                # Remove from ring
                try:
                    self.ring.remove((hash_value, node))
                except ValueError:
                    pass  # Already removed
        
        # Remove from nodes dict
        del self.nodes[node_id]
        return node
    
    def get_node_for_key(self, key: str) -> Optional[Node]:
        """
        Find the node responsible for a given key.
        
        Args:
            key: The key to find a node for
            
        Returns:
            The node responsible for the key, or None if no nodes
        """
        if not self.ring:
            return None
        
        key_hash = self._hash_key(key)
        
        # Binary search for the first node with hash >= key_hash
        index = bisect.bisect_right(self.ring, (key_hash, None))
        
        # If we're past the end, wrap around to the beginning
        if index >= len(self.ring):
            index = 0
        
        return self.ring[index][1]
    
    def get_key_distribution(self, keys: List[str]) -> Dict[str, List[str]]:
        """
        Get the distribution of keys across nodes.
        
        Args:
            keys: List of keys to distribute
            
        Returns:
            Dictionary mapping node_id to list of keys assigned to that node
        """
        distribution = defaultdict(list)
        
        for key in keys:
            node = self.get_node_for_key(key)
            if node:
                distribution[node.node_id].append(key)
        
        return dict(distribution)
    
    def get_moved_keys(self, old_distribution: Dict[str, List[str]], 
                      new_distribution: Dict[str, List[str]]) -> List[str]:
        """
        Find keys that moved between two distributions.
        
        Args:
            old_distribution: Previous key distribution
            new_distribution: Current key distribution
            
        Returns:
            List of keys that moved to different nodes
        """
        moved_keys = []
        
        # Create reverse mapping: key -> node_id
        old_key_to_node = {}
        for node_id, keys in old_distribution.items():
            for key in keys:
                old_key_to_node[key] = node_id
        
        new_key_to_node = {}
        for node_id, keys in new_distribution.items():
            for key in keys:
                new_key_to_node[key] = node_id
        
        # Find keys that changed nodes
        all_keys = set(old_key_to_node.keys()) | set(new_key_to_node.keys())
        for key in all_keys:
            old_node = old_key_to_node.get(key)
            new_node = new_key_to_node.get(key)
            if old_node != new_node:
                moved_keys.append(key)
        
        return moved_keys
    
    def _hash_key(self, key: str) -> int:
        """
        Hash a key using the ring's hash function.
        
        Args:
            key: Key to hash
            
        Returns:
            Hash value for the key
        """
        if self.hash_function == "sha256":
            return int(hashlib.sha256(key.encode()).hexdigest(), 16)
        elif self.hash_function == "fnv1a":
            # Simple FNV-1a implementation
            hash_value = 2166136261  # FNV offset basis
            for byte in key.encode():
                hash_value ^= byte
                hash_value *= 16777619  # FNV prime
                hash_value &= 0xFFFFFFFF  # Keep it 32-bit
            return hash_value
        else:
            raise ValueError(f"Unsupported hash function: {self.hash_function}")
    
    def get_ring_state(self) -> List[Tuple[int, str]]:
        """
        Get the current state of the ring.
        
        Returns:
            List of (hash_value, node_id) tuples sorted by hash value
        """
        return [(hash_val, node.node_id) for hash_val, node in self.ring]
    
    def __len__(self) -> int:
        """Get the number of unique nodes in the ring."""
        return len(self.nodes)
    
    def __str__(self) -> str:
        """String representation of the ring."""
        if not self.ring:
            return "Empty ring"
        return f"Ring with {len(self.nodes)} nodes and {len(self.ring)} hash points"
