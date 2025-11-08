#!/bin/bash

# Consistent Hash Lab - Quick Start Script

echo "Consistent Hash Lab - Quick Start"
echo "======================================"

# Function to run docker-compose with proper warning suppression
run_docker() {
    docker-compose run --rm consistent-hash-lab "$@" 2>/dev/null
}

case "$1" in
    "build")
        echo "Building Docker container..."
        docker-compose build
        ;;
    "demo")
        echo "Running demo with default settings (4 nodes, 10000 keys)..."
        run_docker python demo.py demo "${@:2}"
        ;;
    "test")
        echo "Running unit tests..."
        run_docker python -m pytest tests/ -v
        ;;
    "benchmark")
        echo "Running benchmark..."
        run_docker python demo.py benchmark "${@:2}"
        ;;
    "interactive")
        echo "Starting interactive mode..."
        run_docker python demo.py demo --interactive "${@:2}"
        ;;
    "shell")
        echo "Starting interactive shell in container..."
        docker-compose run --rm consistent-hash-lab bash
        ;;
    *)
        echo "Usage: $0 {build|demo|test|benchmark|interactive|shell} [additional args]"
        echo ""
        echo "Examples:"
        echo "  $0 build                                    # Build the Docker container"
        echo "  $0 demo                                     # Run demo with defaults"
        echo "  $0 demo --nodes 6 --keys 50000             # Run demo with custom settings"
        echo "  $0 test                                     # Run unit tests"
        echo "  $0 benchmark --min-nodes 2 --max-nodes 10  # Run benchmark"
        echo "  $0 interactive --nodes 4                   # Run in interactive mode"
        echo "  $0 shell                                    # Open container shell"
        ;;
esac
