import io
import numpy as np
from PIL import Image

# UDF to process images
def process_image(image_bytes):
    try:
        # Read image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to grayscale
        image = image.convert('L')
        # Resize image
        image = image.resize((256, 256))
        # Normalize pixel values
        image = np.array(image) / 255.0
        return image.tobytes()
    except Exception as e:
        return None