# Disaster Context Graph RAG Implementation Plan

## Goal Description
The goal is to build a "Disaster Context Graph RAG" system. This system involves a two-layer context graph (Schema Graph and Evidence Graph) to improve Retrieval Augmented Generation (RAG) for disaster-related queries.
The system will integrate with an NL-to-SQL agent, an Orchestrator, and a Visualization Layer.

**Key Deliverables:**
1.  **Schema Graph**: Feature nodes, concept/synonym nodes, QuerySpec nodes.
2.  **Evidence Graph**: Document and Chunk nodes, edges to HazardGroup/AdminArea.
3.  **Feature Resolver**: API to map NL to feature_ids.
4.  **Query Router**: Service to match user intents to query specs.
5.  **Learned Edges**: Similarity edges.
6.  **Benchmark Dataset**: 500+ NL queries.

## User Review Required
> [!IMPORTANT]
> **Environment**: A dedicated conda environment `disaster_graph_rag` has been created with `pandas`, `pyarrow`, and `fastparquet`.
> **Dataset**: Dataset is located at `disaster_ai_sp26/datasets`. It consists of 35+ Parquet files aggregated by `hex_id` (H3 index).
> **Key Data Sources**:
> - `CRIT_LIFE_*.parquet`: Critical infrastructure (Hospitals, Grocery).
> - `HIFLD-*.parquet`: Emergency shelters, Fire stations.
> - `EX_BLD_*.parquet`: Building counts.

## Proposed Changes

### Team Assignments (Proposed)
- **User (Lead)**: 
    - **Orchestrator**: Integration of SQL/RAG/Graph.
    - **Architecture**: Defining the overall system interfaces.
- **Ankit (Research Scientist)**: 
    - **Feature Resolver**: Logic to map NL queries (e.g., "places with high hospital access") to dataset columns (e.g., `hex_fc_rac_hospital`).
    - **Learned Edges**: Similarity modeling.
- **Sahil (Master's Student)**: 
    - **Schema Graph**: defining `Feature` nodes for each column in the Parquet files.
    - **Query Library**: Creating SQL templates for hex-based aggregation.
- **Christian (Master's Student)**: 
    - **Evidence Graph**: Ingestion pipeline to load Parquet data into the graph.
    - **Data Processing**: Handling the 13M+ hex rows and optimizing storage.

### Timeline (Next Few Weeks)
### Detailed Weekly Breakdown (Weeks 1-4)

#### **1. Sahil (Master's Student) - The Schema Architect**
**Role**: Define the "Ontology" in Neo4j (The Vocabulary).
*   **Week 1: Initial Nodes**
    *   **Goal**: Create `FeatureNode` definitions just for Critical Infrastructure and Shelter datasets.
    *   **Task**: Edit `src/schema_node.py` to create a `HospitalFeature` and `ShelterFeature` class.
    *   **Task**: Write a script `scripts/build_schema.py` that connects to Neo4j and creates these 2 nodes.
*   **Week 2: Aggregation Rules**
    *   **Goal**: Ensure math is correct.
    *   **Task**: Define `AggregationNode` in Neo4j with properties `formula="SUM(x)"` or `formula="AVG(x)"`.
    *   **Task**: Create standard SQL templates for these rules in a new file `src/query_templates.py`.
*   **Week 3: Query Spec**
    *   **Goal**: Link Features to SQL.
    *   **Task**: Create edges `(:Feature)-[:REQUIRES]->(:Aggregation)` in `scripts/build_schema.py`.

#### **2. Christian (Master's Student) - The Data Engineer**
**Role**: Build the "Evidence Graph" & Ingestion (The Scale).
*   **Week 1: Data Loader**
    *   **Goal**: Read the Parquet files efficiently.
    *   **Task**: Create `src/data_loader.py` using `duckdb` to query `disaster_ai_sp26/datasets/*.parquet`.
    *   **Success Criteria**: A function `get_hex_data(feature_name, hex_ids)` returns a Pandas DataFrame.
*   **Week 2: Evidence Nodes**
    *   **Goal**: Populate Neo4j with "Pointer" nodes.
    *   **Task**: Write `scripts/ingest_evidence.py` to scan the `datasets/` folder and create one `(:Evidence)` node per file in Neo4j.
    *   **Task**: Add properties like `temporal_resolution="daily"` to these nodes.
*   **Week 3: Optimization**
    *   **Goal**: Speed up queries.
    *   **Task**: Experiment with DuckDB indexing on `hex_id` to ensure sub-100ms lookups.

#### **3. Ankit (Research Scientist) - The AI Researcher**
**Role**: The "Feature Resolver" (The Brain).
*   **Week 1: Zero-Shot Baseline**
    *   **Goal**: Map text to columns without training.
    *   **Task**: Install `sentence-transformers`.
    *   **Task**: Update `scripts/learn_edges.py` to run on the real `CRIT_LIFE` column names.
    *   **Deliverable**: A CSV file `learned_edges.csv` containing `(QueryTerm, Column, Score)`.
*   **Week 2: The Resolver API**
    *   **Goal**: A callable Python function for the Orchestrator.
    *   **Task**: Create `src/resolver.py`. Function `resolve_intent(user_query) -> List[FeatureNode]`.
    *   **Task**: Implement a threshold (e.g., score > 0.8) to filter bad matches.
*   **Week 3: Evaluation**
    *   **Goal**: Measure performance.
    *   **Task**: Create a test set of 50 mocked queries (e.g., "Where can I get medical help?") and measure how often it maps to `hex_fc_rac_hospital`.

#### **4. User (Team Lead) - The Orchestrator**
**Role**: System Integration & Architecture.
*   **Week 1: Infrastructure**
    *   **Task**: Dockerize the Neo4j setup (`docker-compose.yml`).
    *   **Task**: Review Sahil's Schema design and Christian's Data Loader.
*   **Week 2: The "SQL Agent"**
    *   **Task**: Create `src/sql_agent.py`. It should take a `QuerySpec` (from Sahil) and run it against Data (from Christian).
    *   **Task**: Implement the "Left/Right Route" logic in code.
*   **Week 3: End-to-End MVP**
    *   **Goal**: The "skeleton run".
    *   **Task**: Write `main.py` that takes "Show me shelters", calls Ankit's Resolver, looks up Sahil's Schema, and runs Christian's Data Loader.

### File Structure
- `scripts/`: Data ingest and graph construction scripts.
- `src/`: Core logic for Resolver, Router, and Graph.
- `guides/`: Documentation.
- `notebooks/`: Exploratory analysis.

## Verification Plan
### Automated Tests
- Unit tests for Graph Node creation.
- API tests for Feature Resolver.
- Data integrity checks for Parquet file loading.

### Manual Verification
- Verify Graph connectivity using sample queries.
- Manually spot-check parsed documents against source PDFs.
