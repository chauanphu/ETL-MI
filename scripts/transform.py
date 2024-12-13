from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, input_file_name
from pyspark.sql.types import BinaryType, StringType
import nibabel as nib
import base64
from cryptography.fernet import Fernet
import io

def load_nifti_and_encrypt(file_path: str, encryption_key: str) -> bytes:
    # Load the NIfTI image using nibabel
    img = nib.load(file_path)

    # Convert the image data into a byte stream
    # NIfTI images are typically 3D arrays and metadata.
    # You can write the entire NIfTI image (header + data) to a byte buffer:
    buffer = io.BytesIO()
    nib.save(img, buffer)
    raw_bytes = buffer.getvalue()
    
    # Encrypt using Fernet (symmetric encryption)
    f = Fernet(encryption_key)
    encrypted_bytes = f.encrypt(raw_bytes)
    
    return encrypted_bytes

# UDF wrapping
def encrypt_file_udf(encryption_key: str):
    def inner(file_path: str) -> bytes:
        return load_nifti_and_encrypt(file_path, encryption_key)
    return inner