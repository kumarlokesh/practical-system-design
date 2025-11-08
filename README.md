# Practical System Design

Bridging the gap between theory and practice in system design.

## Table of Contents

- [Practical System Design](#practical-system-design)
  - [Table of Contents](#table-of-contents)
  - [Go Projects](#go-projects)
    - [AI Code Assistant](#ai-code-assistant)
    - [Kafka Transactional Messaging](#kafka-transactional-messaging)
    - [Write-Ahead Log](#write-ahead-log)
    - [S3 Clone](#s3-clone)
    - [Kubernetes Controller](#kubernetes-controller)
    - [SQL Parser](#sql-parser)
    - [Cassandra SSTable](#cassandra-sstable)
    - [HNSW Vector Search](#hnsw-vector-search)
  - [Rust Projects](#rust-projects)
    - [LLM from Scratch](#llm-from-scratch)
    - [RocksDB Clone](#rocksdb-clone)
    - [SIMD POC](#simd-poc)
  - [Python Projects](#python-projects)
    - [Consistent Hashing Lab](#consistent-hashing-lab)
  - [How to Use](#how-to-use)
  - [License](#license)

Practical System Design is a collection of hands-on exercises and small subprojects that demonstrate core distributed systems and systems-programming concepts. Each exercise is a self-contained folder or repository with its own README and instructions.

## Go Projects

### AI Code Assistant

An exercise demonstrating building an AI-powered coding assistant. [View code](./go/ai-code-assistant/)

### Kafka Transactional Messaging

Reliable message processing using Kafka transactions. [View code](./go/kafka-transactional-messaging/)

### Write-Ahead Log

A low-level WAL implementation for durability and recovery. [View code](./go/wal/)

### S3 Clone

A minimal S3-compatible object storage implementation. [View code](./go/s3-clone/)

### Kubernetes Controller

A controller that manages custom Task resources. [View code](./go/k8s-controller/)

### SQL Parser

A simplified SQL parser and related tooling. [View code](./go/sql-parser/)

### Cassandra SSTable

A simplified SSTable storage format implementation. [View code](./go/cassandra-sstable/)

### HNSW Vector Search

An HNSW approximate nearest-neighbor implementation. [View code](./go/hnsw-poc/)

## Rust Projects

### LLM from Scratch

Step-by-step language model implementation and experiments. [View code](./rust/llm-from-scratch/)

### RocksDB Clone

A key-value store focused on LSM/compaction and SSTables. [View code](./rust/rocksdb-clone/)

### SIMD POC

Proofs-of-concept and benchmarks for SIMD optimizations. [View code](./rust/simd-poc/)

## Python Projects

### Consistent Hashing Lab

An implementation of consistent hashing with configurable virtual nodes and visualization. [View code](./python/consistent_hash_lab/)

## How to Use

Each subproject includes its own README with exact setup and run instructions. General quick-start:

For Go projects:

```bash
# run tests for a Go project
cd go/<project>
go test ./...
```

For Rust projects:

```bash
# run tests for a Rust project
cd rust/<project>
cargo test
```

For Python projects:

```bash
# run tests for a Python project
cd python/<project>
python -m pytest
```

## License

This repository is available under the MIT License. See the `LICENSE` file at the repository root for details.
