# Disaster Context Graph RAG

A two-layer context graph system (Schema Graph + Evidence Graph) for improving RAG on disaster-related queries.

## Quick Start

```bash
# 1. Activate environment
conda activate disaster_graph_rag

# 2. Start Neo4j (requires Docker)
docker-compose up -d

# 3. Build the schema
python scripts/build_schema.py

# 4. Run the demo
python main.py "Where are the shelters?"
```

## Project Structure

```
├── src/
│   ├── graph/           # Neo4j connection & node definitions (Sahil)
│   ├── resolver/        # Feature Resolver & learned edges (Ankit)
│   └── agent/           # SQL Agent & Orchestrator (Lead)
├── scripts/
│   ├── build_schema.py  # Populate Schema Graph
│   ├── ingest_evidence.py # Populate Evidence Graph (Christian)
│   └── learn_edges.py   # Generate similarity edges
├── config/
│   └── schema.yaml      # Feature & Concept definitions
├── tests/               # Unit tests
├── plan/                # Implementation plans
└── Guides/              # Documentation
```

## Team

| Member    | Role               | Focus Area                     |
|-----------|--------------------|--------------------------------|
| Lead      | Orchestrator       | System Integration, SQL Agent  |
| Ankit     | Research Scientist | Feature Resolver, Learned Edges|
| Sahil     | MS Student         | Schema Graph, Query Library    |
| Christian | MS Student         | Evidence Graph, Data Ingestion |

## Environment

```bash
conda create -n disaster_graph_rag python=3.10 pandas pyarrow duckdb
conda activate disaster_graph_rag
pip install neo4j sentence-transformers
```
