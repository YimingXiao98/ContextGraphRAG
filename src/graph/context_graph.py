"""
Neo4j Graph Connection & Schema Management (Sahil)
"""
from neo4j import GraphDatabase
import yaml
from pathlib import Path


class ContextGraph:
    """Connection manager for the Neo4j Context Graph."""

    def __init__(self, uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", 
                 password: str = "password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_graph(self):
        """Remove all nodes and edges. Use with caution."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_feature(self, feature_id: str, name: str, source: str, 
                       aggregation: str, description: str = ""):
        """Create a Feature node in the Schema Graph."""
        query = """
        MERGE (f:Feature {id: $id})
        SET f.name = $name, f.source = $source, 
            f.aggregation = $agg, f.description = $desc
        """
        with self.driver.session() as session:
            session.run(query, id=feature_id, name=name, 
                       source=source, agg=aggregation, desc=description)

    def create_concept(self, concept_id: str, name: str, synonyms: list):
        """Create a Concept node and link synonyms."""
        query = """
        MERGE (c:Concept {id: $id})
        SET c.name = $name, c.synonyms = $synonyms
        """
        with self.driver.session() as session:
            session.run(query, id=concept_id, name=name, synonyms=synonyms)

    def link_concept_to_feature(self, concept_id: str, feature_id: str):
        """Create MAPS_TO edge between Concept and Feature."""
        query = """
        MATCH (c:Concept {id: $c_id}), (f:Feature {id: $f_id})
        MERGE (c)-[:MAPS_TO]->(f)
        """
        with self.driver.session() as session:
            session.run(query, c_id=concept_id, f_id=feature_id)

    def resolve_concept(self, concept_name: str) -> list:
        """Given a concept name, return linked Feature IDs."""
        query = """
        MATCH (c:Concept)-[:MAPS_TO]->(f:Feature)
        WHERE toLower(c.name) = toLower($name) 
           OR $name IN [s IN c.synonyms | toLower(s)]
        RETURN f.id as feature_id, f.source as source, f.aggregation as agg
        """
        with self.driver.session() as session:
            result = session.run(query, name=concept_name)
            return [dict(record) for record in result]


def load_schema_from_yaml(yaml_path: str = "config/schema.yaml") -> dict:
    """Load schema definition from YAML file."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    # Quick test
    print("Testing ContextGraph connection...")
    # graph = ContextGraph()
    # graph.close()
    print("Module loaded successfully. Neo4j connection not tested (requires running instance).")
