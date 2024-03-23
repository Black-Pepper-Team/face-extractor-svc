from __future__ import annotations

import numpy as np
import face_recognition
from enum import Enum
from typing import List, Tuple, Annotated

class FaceExtractionStatus(Enum):
    """
    List of statuses for face extraction
    """
    SUCCESS = 0
    NO_FACE_FOUND = 1
    TOO_MANY_PEOPLE = 2

FeatureVector = Annotated[List[float], 128]
DiscretizedFeatureVector = Annotated[List[int], 128]
      
class FeatureExtractor:
    """
    Class responsible for extracting features from the image
    """
      
    def __init__(self, img: np.ndarray):
        self._img = img

    def extract_features(self) -> Tuple[FeatureVector, FaceExtractionStatus]:
        """
        Extracts features from the image. Returns the feature vector and the status of the extraction.
        If extraction is unsuccessful, the feature vector will be `None`.
        """
        
        NUM_JUTTERS = 2 # More gives better accuracy but slower processing
            
        embeddings = face_recognition.face_encodings(self._img, 
                                                    known_face_locations=None,
                                                    num_jitters=NUM_JUTTERS)
        
        match len(embeddings):
            case 0:
                return None, FaceExtractionStatus.NO_FACE_FOUND
            case 1:
                embedding = embeddings[0]
                embedding_as_float = [float(i) for i in embedding]
                return embedding_as_float, FaceExtractionStatus.SUCCESS
            case _:
                return None, FaceExtractionStatus.TOO_MANY_PEOPLE
    
    @staticmethod
    def _discretize_embedding(embedding: FeatureVector) -> DiscretizedFeatureVector:
        """
        Discretizes the embedding
        """
        MUL_FACTOR: int = 127
        
        return [int((i + 1) * MUL_FACTOR) for i in embedding]
            
    def extract_discrete_features(self) -> Tuple[DiscretizedFeatureVector, FaceExtractionStatus]:
        """
        Extracts features from the image and discretizes them. 
        Returns the feature vector and the status of the extraction.
        If extraction is unsuccessful, the feature vector will be `None`.
        """
        
        emb, status = self.extract_features()
        if status == FaceExtractionStatus.TOO_MANY_PEOPLE or status == FaceExtractionStatus.NO_FACE_FOUND:
            return emb, status
        
        return FeatureExtractor._discretize_embedding(emb), status
        
