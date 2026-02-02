"""
Disaster Context Graph RAG - Main Orchestrator
"""
import yaml
from pathlib import Path

from src.resolver.feature_resolver import FeatureResolver
from src.agent.sql_agent import SQLAgent


def load_features_from_yaml(yaml_path: str = "config/schema.yaml") -> list:
    """Load feature definitions from schema YAML."""
    with open(yaml_path, 'r') as f:
        schema = yaml.safe_load(f)
    return schema.get('features', [])


def main(query: str):
    """
    End-to-end flow:
    1. Resolve query to features (Ankit's Resolver)
    2. Execute against data (Christian's Loader via SQL Agent)
    """
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    # Step 1: Load features and initialize resolver
    print("\n[1] Loading features from schema...")
    features = load_features_from_yaml()
    
    resolver = FeatureResolver()
    resolver.load_features(features)
    
    # Step 2: Resolve query to features
    print(f"[2] Resolving query: '{query}'")
    resolved = resolver.resolve(query)
    
    if not resolved:
        print("❌ No matching features found.")
        return
    
    print(f"    Found {len(resolved)} matching feature(s):")
    for r in resolved:
        print(f"      - {r.feature_id} (score: {r.score:.2f})")
    
    # Step 3: Execute query via SQL Agent
    print(f"\n[3] Executing query via SQL Agent...")
    agent = SQLAgent()
    
    best_match = resolved[0]
    result = agent.execute_from_resolved(best_match)
    
    print(f"\n{'='*60}")
    print(f"Result: {result['value']}")
    print(f"Feature: {result['feature']}")
    print(f"Aggregation: {result['aggregation']}")
    print(f"Source: {result['source']}")
    print(f"{'='*60}")
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Where are the emergency shelters?"
    
    main(query)
