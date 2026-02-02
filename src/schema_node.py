from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SchemaNode:
    """Base class for all schema nodes."""
    id: str
    description: str

@dataclass
class FeatureNode(SchemaNode):
    """Represents a feature in the dataset (e.g., a column in a parquet file)."""
    source_file: str
    data_type: str
    aggregation_rule: str  # e.g., 'SUM', 'AVG'

@dataclass
class ConceptNode(SchemaNode):
    """Represents a high-level concept (e.g., 'Medical Access')."""
    related_features: List[str]

@dataclass
class QuerySpecNode(SchemaNode):
    """Represents a predefined SQL query template."""
    sql_template: str
