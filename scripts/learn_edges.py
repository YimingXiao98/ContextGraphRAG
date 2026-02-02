import pandas as pd
import numpy as np
try:
    from sentence_transformers import SentenceTransformer, util
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

def calculate_learned_edges(concepts, features, threshold=0.4):
    """
    Demonstrates how to 'learn' edges between Concepts and Features 
    using semantic similarity (Vector Embeddings).
    """
    if not HAS_TRANSFORMERS:
        print("Error: 'sentence-transformers' not found.")
        print("Please install it to run this demo: pip install sentence-transformers")
        # specific fallback for demo purposes if package is missing
        print("\n--- SIMULATED OUTPUT (Logic Demonstration) ---")
        return [
            ("Medical Access", "hex_fc_rac_hospital", 0.85),
            ("High Water", "flood_inundation_depth", 0.78)
        ]

    # 1. Load Pre-trained Model (Zero-Shot)
    # This model has already "learned" English from millions of documents.
    print("Loading pre-trained embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Encode strings to lists of numbers (Vectors)
    print("Encoding concepts and features...")
    concept_embeddings = model.encode(concepts, convert_to_tensor=True)
    feature_embeddings = model.encode(features, convert_to_tensor=True)

    # 3. Calculate Similarity (Cosine Distance)
    # Result is a matrix of scores (0.0 to 1.0)
    cosine_scores = util.cos_sim(concept_embeddings, feature_embeddings)

    learned_edges = []

    # 4. Filter and Create Edges
    print(f"\nScanning for matches (Threshold > {threshold})...")
    for i, concept in enumerate(concepts):
        for j, feature in enumerate(features):
            score = cosine_scores[i][j].item()
            if score > threshold:
                learned_edges.append((concept, feature, score))
    
    return learned_edges

if __name__ == "__main__":
    # Example Data
    concepts = [
        "Medical Access", 
        "High Flood Risk", 
        "Emergency Shelter", 
        "Power Outage"
    ]
    
    features = [
        "hex_fc_rac_hospital",        # Matches Medical
        "flood_inundation_depth",     # Matches Flood
        "hifld_shelter_locations",    # Matches Shelter
        "building_count",             # Noise / Low match
        "road_density_index"          # Noise / Low match
    ]

    print("--- Starting Learned Edges Discovery ---")
    edges = calculate_learned_edges(concepts, features)

    print(f"\nFound {len(edges)} Learned Edges:")
    print(f"{'Concept':<20} | {'Feature':<25} | {'Score':<5}")
    print("-" * 55)
    for concept, feature, score in sorted(edges, key=lambda x: x[2], reverse=True):
        print(f"{concept:<20} | {feature:<25} | {score:.2f}")

    print("\nNext Step: Insert these triplets tuple(Concept, Feature, Score) into Neo4j.")
