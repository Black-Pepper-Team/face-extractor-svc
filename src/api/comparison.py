import ast
import src.extractor.comparison as comparison
from src.extractor.embedding import FeatureVector
from src.model.claim import Claim, select_all_claims

def get_closest_claim(embedding: FeatureVector) -> Claim:
    """
    Returns the closest claim to the given embedding. Returns None if no claim is found.
    """
    
    claims = select_all_claims()
    claim_embeddings = [ast.literal_eval(claim['vector']) for claim in claims]
    
    min_claim, min_dist = None, comparison.INFTY_DIST
    for i, claim_embedding in enumerate(claim_embeddings):
        dist = comparison.get_distance_squared(embedding, claim_embedding)
        if dist < min_dist:
            min_dist = dist
            min_claim = claims[i]
    
    return min_claim

def get_claim_from_embedding(embedding: FeatureVector) -> Claim:
    """
    Returns the claim with the same identity of one in the embedding. If no
    such claim exists, returns None
    """
    
    closest_claim = get_closest_claim(embedding)
    if closest_claim is None:
        return None
    closest_embedding = ast.literal_eval(closest_claim['vector'])
    same_identity = comparison.is_same_identity(embedding, closest_embedding)
    return closest_claim if same_identity else None

def claim_exists(embedding: FeatureVector) -> bool:
    """
    Checks if there is a claim in the database with the same identity as the one in the embedding
    """
    
    return get_claim_from_embedding(embedding) is not None
