"""
SQL Agent - Orchestrates queries (Lead)
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from src.agent.data_loader import DataLoader
from src.resolver.feature_resolver import ResolvedFeature


@dataclass
class QuerySpec:
    """Specification for a data query."""
    feature_id: str
    source_file: str
    aggregation: str
    hex_ids: Optional[List[str]] = None


class SQLAgent:
    """
    Takes resolved features and executes queries against the data.
    This is the "Muscle" that acts on the "Brain's" specifications.
    """

    def __init__(self, data_dir: str = "disaster_ai_sp26/datasets"):
        self.loader = DataLoader(data_dir)

    def execute(self, spec: QuerySpec) -> Dict[str, Any]:
        """
        Execute a query based on the specification.
        
        Args:
            spec: QuerySpec from the resolver/graph
            
        Returns:
            Dict with 'value' and 'metadata'
        """
        # The "Right Route" - Apply the correct aggregation
        result = self.loader.aggregate_feature(
            source_file=spec.source_file,
            feature_column=spec.feature_id,
            aggregation=spec.aggregation,
            hex_ids=spec.hex_ids
        )
        
        return {
            "value": result,
            "feature": spec.feature_id,
            "aggregation": spec.aggregation,
            "source": spec.source_file,
            "hex_filter": len(spec.hex_ids) if spec.hex_ids else "all"
        }

    def execute_from_resolved(self, resolved: ResolvedFeature, 
                               hex_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Convenience method to execute directly from resolver output.
        """
        spec = QuerySpec(
            feature_id=resolved.feature_id,
            source_file=resolved.source,
            aggregation=resolved.aggregation,
            hex_ids=hex_ids
        )
        return self.execute(spec)


if __name__ == "__main__":
    agent = SQLAgent()
    
    # Test query
    spec = QuerySpec(
        feature_id="building_count",
        source_file="EX_BLD_001.parquet",
        aggregation="SUM"
    )
    
    print("Testing SQL Agent...")
    # result = agent.execute(spec)
    # print(f"Result: {result}")
    print("Module loaded successfully.")
