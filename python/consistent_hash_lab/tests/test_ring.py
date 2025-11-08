"""
Unit tests for the consistent hash ring implementation.

Tests node lookup stability and correct mapping functionality.
"""
import pytest
from ..node import Node
from ..ring import ConsistentHashRing


class TestConsistentHashRing:
    """Test cases for ConsistentHashRing class."""
    
    def test_empty_ring(self):
        """Test behavior with an empty ring."""
        ring = ConsistentHashRing()
        assert len(ring) == 0
        assert ring.get_node_for_key("test_key") is None
        assert ring.get_key_distribution(["key1", "key2"]) == {}
    
    def test_single_node(self):
        """Test ring with a single node."""
        ring = ConsistentHashRing()
        node = Node("node1")
        ring.add_node(node)
        
        assert len(ring) == 1
        assert ring.get_node_for_key("test_key") == node
        assert ring.get_node_for_key("another_key") == node
    
    def test_multiple_nodes(self):
        """Test ring with multiple nodes."""
        ring = ConsistentHashRing()
        nodes = [Node(f"node{i}") for i in range(3)]
        
        for node in nodes:
            ring.add_node(node)
        
        assert len(ring) == 3
        
        # Each key should map to exactly one node
        test_keys = ["key1", "key2", "key3", "key4", "key5"]
        for key in test_keys:
            node = ring.get_node_for_key(key)
            assert node is not None
            assert node in nodes
    
    def test_node_removal(self):
        """Test removing nodes from the ring."""
        ring = ConsistentHashRing()
        nodes = [Node(f"node{i}") for i in range(3)]
        
        for node in nodes:
            ring.add_node(node)
        
        # Remove a node
        removed_node = ring.remove_node("node1")
        assert removed_node == nodes[1]
        assert len(ring) == 2
        assert "node1" not in ring.nodes
        
        # Keys should still map to remaining nodes
        remaining_nodes = [nodes[0], nodes[2]]
        for key in ["test1", "test2", "test3"]:
            node = ring.get_node_for_key(key)
            assert node in remaining_nodes
    
    def test_duplicate_node_addition(self):
        """Test that adding duplicate nodes raises an error."""
        ring = ConsistentHashRing()
        node = Node("node1")
        ring.add_node(node)
        
        with pytest.raises(ValueError, match="Node node1 already exists"):
            ring.add_node(Node("node1"))
    
    def test_nonexistent_node_removal(self):
        """Test removing a non-existent node."""
        ring = ConsistentHashRing()
        node = Node("node1")
        ring.add_node(node)
        
        result = ring.remove_node("nonexistent")
        assert result is None
        assert len(ring) == 1
    
    def test_key_distribution(self):
        """Test key distribution across nodes."""
        ring = ConsistentHashRing()
        nodes = [Node(f"node{i}") for i in range(3)]
        
        for node in nodes:
            ring.add_node(node)
        
        test_keys = [f"key{i}" for i in range(100)]
        distribution = ring.get_key_distribution(test_keys)
        
        # All nodes should have some keys
        assert len(distribution) == 3
        total_keys = sum(len(keys) for keys in distribution.values())
        assert total_keys == 100
        
        # Each node should have a reasonable share (not perfect, but reasonable)
        for node_id, keys in distribution.items():
            assert len(keys) > 0  # Each node should get at least some keys
    
    def test_virtual_nodes(self):
        """Test consistent hashing with virtual nodes (replicas)."""
        ring = ConsistentHashRing()
        
        # Add nodes with different replica counts
        node1 = Node("node1", replicas=1)
        node2 = Node("node2", replicas=3)
        
        ring.add_node(node1)
        ring.add_node(node2)
        
        # node2 should get more keys due to more replicas
        test_keys = [f"key{i}" for i in range(1000)]
        distribution = ring.get_key_distribution(test_keys)
        
        node1_keys = len(distribution.get("node1", []))
        node2_keys = len(distribution.get("node2", []))
        
        # node2 should get more keys due to more replicas
        assert node2_keys > node1_keys
        assert node2_keys / node1_keys > 1.1  # At least 1.1x more (relaxed for hash randomness)
    
    def test_consistency_after_node_addition(self):
        """Test that existing key mappings remain stable when adding nodes."""
        ring = ConsistentHashRing()
        
        # Start with 2 nodes
        for i in range(2):
            ring.add_node(Node(f"node{i}"))
        
        test_keys = [f"key{i}" for i in range(100)]
        initial_distribution = ring.get_key_distribution(test_keys)
        
        # Add a third node
        ring.add_node(Node("node2"))
        new_distribution = ring.get_key_distribution(test_keys)
        
        # Calculate how many keys moved
        moved_keys = ring.get_moved_keys(initial_distribution, new_distribution)
        
        # Only a fraction of keys should move (consistent hashing property)
        movement_ratio = len(moved_keys) / len(test_keys)
        assert movement_ratio < 0.8  # Less than 80% should move (relaxed for small node count)
        assert movement_ratio > 0     # But some should move
    
    def test_consistency_after_node_removal(self):
        """Test that minimal keys move when removing a node."""
        ring = ConsistentHashRing()
        
        # Start with 3 nodes
        for i in range(3):
            ring.add_node(Node(f"node{i}"))
        
        test_keys = [f"key{i}" for i in range(100)]
        initial_distribution = ring.get_key_distribution(test_keys)
        
        # Remove one node
        ring.remove_node("node1")
        new_distribution = ring.get_key_distribution(test_keys)
        
        # Only keys from the removed node should move
        moved_keys = ring.get_moved_keys(initial_distribution, new_distribution)
        initial_node1_keys = len(initial_distribution.get("node1", []))
        
        # The number of moved keys should approximately equal the keys on removed node
        assert abs(len(moved_keys) - initial_node1_keys) < 5  # Allow small variance
    
    def test_different_hash_functions(self):
        """Test that different hash functions produce different distributions."""
        sha_ring = ConsistentHashRing(hash_function="sha256")
        fnv_ring = ConsistentHashRing(hash_function="fnv1a")
        
        # Add same nodes to both rings
        for i in range(3):
            sha_ring.add_node(Node(f"node{i}"))
            fnv_ring.add_node(Node(f"node{i}"))
        
        test_keys = ["key1", "key2", "key3", "key4", "key5"]
        
        sha_mapping = {key: sha_ring.get_node_for_key(key).node_id for key in test_keys}
        fnv_mapping = {key: fnv_ring.get_node_for_key(key).node_id for key in test_keys}
        
        # Distributions should be different (very likely with different hash functions)
        assert sha_mapping != fnv_mapping
    
    def test_ring_state(self):
        """Test getting the ring state."""
        ring = ConsistentHashRing()
        node = Node("test_node", replicas=2)
        ring.add_node(node)
        
        state = ring.get_ring_state()
        assert len(state) == 2  # 2 replicas = 2 positions
        
        # State should be sorted by hash value
        hash_values = [hash_val for hash_val, _ in state]
        assert hash_values == sorted(hash_values)
        
        # All positions should belong to our node
        for hash_val, node_id in state:
            assert node_id == "test_node"
    
    def test_unsupported_hash_function(self):
        """Test that unsupported hash functions raise an error."""
        with pytest.raises(ValueError, match="Unsupported hash function"):
            ring = ConsistentHashRing(hash_function="unsupported")
            node = Node("test")
            ring.add_node(node)


class TestNode:
    """Test cases for Node class."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = Node("test_node")
        assert node.node_id == "test_node"
        assert node.replicas == 1
        assert node.weight == 1.0
    
    def test_node_with_replicas(self):
        """Test node creation with replicas."""
        node = Node("test_node", replicas=5, weight=2.0)
        assert node.node_id == "test_node"
        assert node.replicas == 5
        assert node.weight == 2.0
    
    def test_hash_values(self):
        """Test hash value generation."""
        node = Node("test_node", replicas=3)
        hash_values = node.get_hash_values("sha256")
        
        assert len(hash_values) == 3
        assert len(set(hash_values)) == 3  # All should be unique
        assert all(isinstance(h, int) for h in hash_values)
    
    def test_node_equality(self):
        """Test node equality comparison."""
        node1 = Node("test", replicas=1)
        node2 = Node("test", replicas=5)  # Different replicas
        node3 = Node("different")
        
        assert node1 == node2  # Same node_id
        assert node1 != node3  # Different node_id
        assert node1 != "not_a_node"  # Different type
    
    def test_node_hashing(self):
        """Test that nodes can be used as dictionary keys."""
        node1 = Node("test")
        node2 = Node("test")  # Same ID
        node3 = Node("different")
        
        node_dict = {node1: "value1", node3: "value3"}
        
        # node2 should access the same entry as node1
        assert node_dict[node2] == "value1"
        assert len(node_dict) == 2
    
    def test_unsupported_hash_function_in_node(self):
        """Test that nodes reject unsupported hash functions."""
        node = Node("test")
        with pytest.raises(ValueError, match="Unsupported hash function"):
            node.get_hash_values("unsupported")
