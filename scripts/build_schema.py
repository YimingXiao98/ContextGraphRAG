"""
Build Schema - Populate Neo4j from schema.yaml (Sahil)
"""
import yaml
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graph.context_graph import ContextGraph


def build_schema(yaml_path: str = "config/schema.yaml", 
                 clear_existing: bool = False):
    """
    Load schema from YAML and create nodes in Neo4j.
    """
    # Load YAML
    with open(yaml_path, 'r') as f:
        schema = yaml.safe_load(f)
    
    # Connect to Neo4j
    graph = ContextGraph()
    
    if clear_existing:
        print("Clearing existing graph...")
        graph.clear_graph()
    
    # Create Feature nodes
    print(f"Creating {len(schema.get('features', []))} Feature nodes...")
    for feat in schema.get('features', []):
        graph.create_feature(
            feature_id=feat['id'],
            name=feat['name'],
            source=feat['source'],
            aggregation=feat['aggregation'],
            description=feat.get('description', '')
        )
        print(f"  ✓ {feat['id']}")
    
    # Create Concept nodes and link to features
    print(f"Creating {len(schema.get('concepts', []))} Concept nodes...")
    for concept in schema.get('concepts', []):
        graph.create_concept(
            concept_id=concept['id'],
            name=concept['name'],
            synonyms=concept.get('synonyms', [])
        )
        
        # Link to features
        for feat_id in concept.get('maps_to', []):
            graph.link_concept_to_feature(concept['id'], feat_id)
        
        print(f"  ✓ {concept['id']} -> {concept.get('maps_to', [])}")
    
    graph.close()
    print("\nSchema build complete!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true", help="Clear graph first")
    args = parser.parse_args()
    
    build_schema(clear_existing=args.clear)
