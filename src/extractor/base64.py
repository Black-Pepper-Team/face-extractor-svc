import io, base64
import numpy as np
from PIL import Image

def decode_base64(base64_str: str) -> np.ndarray:
    """
    Decodes a base64 string into a numpy array
    """
    ENCODING = "utf-8"
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, ENCODING))))
    return np.array(img)