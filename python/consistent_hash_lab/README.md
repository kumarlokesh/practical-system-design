# Consistent Hash Lab

A hands-on implementation and visualization of consistent hashing, exploring how systems balance keys and minimize data movement.

## Overview

This lab provides tools to understand consistent hashing through code and visualization, measure balance and stability, and explore variations like virtual nodes and weighted nodes.

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed

### Running the Lab

1. **Build and start the container:**

   ```bash
   docker-compose up --build -d
   ```

2. **Enter the container:**

   ```bash
   docker-compose exec consistent-hash-lab bash
   ```

3. **Run the demo:**

   ```bash
   python -m consistent_hash_lab.demo --nodes 4 --keys 10000
   ```

### Available Commands

#### Basic Demo

```bash
# Run with default settings (4 nodes, 10000 keys)
python -m consistent_hash_lab.demo

# Customize parameters
python -m consistent_hash_lab.demo --nodes 6 --keys 50000 --hash sha256 --virtual-nodes 3

# Interactive mode for adding/removing nodes
python -m consistent_hash_lab.demo --interactive
```

#### Benchmark Mode

```bash
# Benchmark different node counts
python -m consistent_hash_lab.demo benchmark --min-nodes 2 --max-nodes 20 --keys 10000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=consistent_hash_lab

# Run specific test file
pytest tests/test_ring.py -v
```

## Project Structure

```
consistent_hash_lab/
├── __init__.py          # Package initialization
├── node.py              # Node class with virtual replicas
├── ring.py              # Consistent hash ring implementation
├── demo.py              # CLI demonstration tool
├── tests/               # Unit tests
│   ├── test_ring.py     # Ring functionality tests
│   └── __init__.py
├── Dockerfile           # Container setup
├── docker-compose.yml   # Development environment
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features

### Phase 1 - Core Implementation ✅

- **Node Management**: Add/remove nodes with virtual replicas
- **Key Distribution**: Consistent key-to-node mapping
- **CLI Demo**: Interactive demonstration with rich output
- **Unit Tests**: Comprehensive test coverage

### Phase 2 - Metrics & Analysis (Coming Soon)

- Balance scoring and distribution analysis
- Key movement measurement on topology changes
- Comparison with baseline hash-based sharding

### Phase 3 - Visualization (Coming Soon)

- Visual hash ring representation
- Animation of node additions/removals
- Key placement visualization

## Tech Stack

| Purpose | Library |
|---------|---------|
| Hashing | hashlib, mmh3 |
| CLI | typer |
| Pretty Output | rich |
| Testing | pytest |
| Visualization | matplotlib, networkx (planned) |
| Metrics | numpy (planned) |

## Example Output

```
Consistent Hash Lab Demo
Configuration: Nodes: 4 | Keys: 10,000 | Hash: sha256 | Virtual nodes: 1

Creating nodes...
  ✓ Added Node(node-00, replicas=1, weight=1.0)
  ✓ Added Node(node-01, replicas=1, weight=1.0)
  ✓ Added Node(node-02, replicas=1, weight=1.0)
  ✓ Added Node(node-03, replicas=1, weight=1.0)

Key Distribution:
┌─────────────────┬───────┬────────────┬──────────────────────┐
│ Node ID         │  Keys │ Percentage │ Load Bar             │
├─────────────────┼───────┼────────────┼──────────────────────┤
│ node-02         │ 2,847 │  28.47%    │ ████████████████████ │
│ node-01         │ 2,503 │  25.03%    │ █████████████████░░░ │
│ node-00         │ 2,425 │  24.25%    │ ████████████████░░░░ │
│ node-03         │ 2,225 │  22.25%    │ ███████████████░░░░░ │
└─────────────────┴───────┴────────────┴──────────────────────┘

Balance Statistics:
  Average: 2500.0 keys per node
  Range: 2,225 - 2,847 keys
  Balance ratio: 1.14x
```

## Interactive Mode

The interactive mode allows real-time manipulation of the hash ring:

```bash
python -m consistent_hash_lab.demo --interactive

Interactive Mode
Commands: add <node_id>, remove <node_id>, status, quit

> add node-new
✓ Added node node-new
Impact: 1,847 keys moved (18.47%)

> remove node-01
✓ Removed node node-01
Impact: 2,503 keys moved (25.03%)

> status
# Shows current distribution and total movement since start
```

## Development

### Adding New Features

1. **Implement in the container:**

   ```bash
   docker-compose exec consistent-hash-lab bash
   ```

2. **Run tests after changes:**

   ```bash
   pytest tests/ -v
   ```

3. **Test CLI changes:**

   ```bash
   python -m consistent_hash_lab.demo --help
   ```

### Container Management

```bash
# Rebuild after dependency changes
docker-compose down
docker-compose up --build

# View logs
docker-compose logs

# Clean up
docker-compose down --volumes --rmi local
```

## Goals

This lab demonstrates:

- **Consistent Hashing Fundamentals**: How keys map to nodes
- **Stability**: Minimal key movement on topology changes  
- **Load Balancing**: Distribution evenness across nodes
- **Virtual Nodes**: Improving balance with replicas
- **Hash Functions**: Impact of different algorithms
