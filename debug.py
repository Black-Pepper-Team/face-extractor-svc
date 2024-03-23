# --- This file contains debugging commands for the feature extractor service ---

# For debugging purposes
import io, base64
from PIL import Image

# Some ML magic
import numpy as np
import face_recognition

# API + CLI imports
import typer
from typing_extensions import Annotated
from pathlib import Path

# Internal imports
from src.extractor.embedding import FeatureExtractor

def debug_embeddings(
        img_1_path: Annotated[Path, typer.Option(help='Path to image 1')] = 'test/anton_1.jpg',
        img_2_path: Annotated[Path, typer.Option(help='Path to image 2')] = 'test/ivan_1.jpg',
    ) -> None:
    """
    Command just for debugging purposes to see how embeddings are extracted and compared
    """
    
    img_1 = face_recognition.load_image_file(img_1_path)
    img_2 = face_recognition.load_image_file(img_2_path)

    extractor_1 = FeatureExtractor(img_1)
    extractor_2 = FeatureExtractor(img_2)
    
    embedding_1, status_1 = extractor_1.extract_features()
    embedding_2, status_2 = extractor_2.extract_features()
    
    print(f'Extraction status 1: {status_1}')
    print(f'Embedding 1: {embedding_1}')
    print(f'Extraction status 2: {status_2}')
    print(f'Embedding 2: {embedding_2}')

    distance = np.sum(np.square(np.array(embedding_1) - np.array(embedding_2)))
    print(f'Distance is: {distance}')


def debug_discrete_embeddings(
        img_1_path: Annotated[Path, typer.Option(help='Path to image 1')] = 'test/ivan_1.jpg',
        img_2_path: Annotated[Path, typer.Option(help='Path to image 2')] = 'test/ivan_2.jpg',
    ) -> None:
    """
    Command just for debugging purposes to see how discrete embeddings are extracted and compared
    """
    
    img_1 = face_recognition.load_image_file(img_1_path)
    img_2 = face_recognition.load_image_file(img_2_path)

    extractor_1 = FeatureExtractor(img_1)
    extractor_2 = FeatureExtractor(img_2)
    
    embedding_1, status_1 = extractor_1.extract_discrete_features()
    embedding_2, status_2 = extractor_2.extract_discrete_features()
    
    print(f'Extraction status 1: {status_1}')
    print(f'Embedding 1: {embedding_1}')
    print(f'Extraction status 2: {status_2}')
    print(f'Embedding 2: {embedding_2}')

    distance = np.sum(np.square(np.array(embedding_1) - np.array(embedding_2)))
    print(f'Distance is: {distance}')
    
    
def debug_encode(img_path: Annotated[Path, typer.Argument(help='Path to image')]) -> None:
    """
    Command just for debugging purposes to test how encoding works
    """
    
    img = Image.open(img_path)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    with open('encoded.txt', 'wb') as f:
        f.write(img_str)
    

def debug_show_npy_img(img_path: Annotated[Path, typer.Argument(help='Path to image')]) -> None:
    """
    Command just for debugging purposes to test how encoding works
    """
    
    img = np.load(img_path)
    img = Image.fromarray(img)
    img.show()