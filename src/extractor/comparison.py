import numpy as np
from src.extractor.embedding import FeatureVector

THRESHOLD = 0.3
INFTY_DIST = 1e8 # This value is larger than all possible distances

def get_distance_squared(embedding_1: FeatureVector, embedding_2: FeatureVector) -> float:
    """
    Returns the distance between two embeddings
    """
    return np.sum(np.square(np.array(embedding_1) - np.array(embedding_2)))

def is_same_identity(embedding_1: FeatureVector, embedding_2: FeatureVector) -> bool:
    """
    Checks if two embeddings belong to the same person
    """
    
    return get_distance_squared(embedding_1, embedding_2) < THRESHOLD**2