"""
Feature Resolver - Maps NL queries to Feature nodes (Ankit)
"""
from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from sentence_transformers import SentenceTransformer, util
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False


@dataclass
class ResolvedFeature:
    """Result of resolving a user query to a feature."""
    feature_id: str
    score: float
    source: str
    aggregation: str


class FeatureResolver:
    """
    Resolves natural language queries to database features.
    Uses pre-trained embeddings for semantic matching.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        self.feature_embeddings = None
        self.features = []
        
        if HAS_TRANSFORMERS:
            self.model = SentenceTransformer(model_name)

    def load_features(self, features: List[Dict]):
        """
        Load feature definitions and compute embeddings.
        
        Args:
            features: List of dicts with 'id', 'name', 'source', 'aggregation'
        """
        self.features = features
        if self.model:
            # Create searchable text from feature name and description
            texts = [f"{feat['name']} {feat.get('description', '')}" 
                    for feat in features]
            self.feature_embeddings = self.model.encode(texts, convert_to_tensor=True)

    def resolve(self, query: str, threshold: float = 0.4) -> List[ResolvedFeature]:
        """
        Resolve a natural language query to matching features.
        
        Args:
            query: User's natural language query
            threshold: Minimum similarity score (0-1)
            
        Returns:
            List of ResolvedFeature sorted by score descending
        """
        if not self.model or self.feature_embeddings is None:
            # Fallback: simple keyword matching
            return self._keyword_match(query)

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.feature_embeddings)[0]

        results = []
        for idx, score in enumerate(scores):
            if score.item() > threshold:
                feat = self.features[idx]
                results.append(ResolvedFeature(
                    feature_id=feat['id'],
                    score=score.item(),
                    source=feat['source'],
                    aggregation=feat['aggregation']
                ))

        return sorted(results, key=lambda x: x.score, reverse=True)

    def _keyword_match(self, query: str) -> List[ResolvedFeature]:
        """Simple keyword fallback when no model is available."""
        query_lower = query.lower()
        results = []
        for feat in self.features:
            name_lower = feat['name'].lower()
            if any(word in query_lower for word in name_lower.split()):
                results.append(ResolvedFeature(
                    feature_id=feat['id'],
                    score=0.5,  # Default score for keyword match
                    source=feat['source'],
                    aggregation=feat['aggregation']
                ))
        return results


if __name__ == "__main__":
    # Demo usage
    resolver = FeatureResolver()
    
    sample_features = [
        {"id": "hex_fc_rac_hospital", "name": "Hospital Access", 
         "source": "CRIT_LIFE.parquet", "aggregation": "AVG"},
        {"id": "hifld_shelter_n", "name": "Shelter Count",
         "source": "HIFLD.parquet", "aggregation": "SUM"},
    ]
    
    resolver.load_features(sample_features)
    
    results = resolver.resolve("Where can I find emergency shelters?")
    for r in results:
        print(f"{r.feature_id}: {r.score:.2f}")
