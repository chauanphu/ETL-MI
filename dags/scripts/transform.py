from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
from airflow.decorators import task
import os
import logging
import cv2
from pyspark.rdd import RDD
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task.pyspark(conn_id='NIfTI_Processing')
def resize_image(image_rdds: RDD):
    def resize_image(x):
        image_data, header, affine, file_name = x
        resized_image = cv2.resize(image_data, (256, 256))
        return resized_image, header, affine, file_name
    
    resized_image_rdds = image_rdds.map(resize_image)
    logger.info("Image resized successfully!")
    return resized_image_rdds

# Normalize the image data
@task.pyspark(conn_id='NIfTI_Processing')
def normalize_image(image_rdds: RDD):
    def normalize_image(x):
        image_data, header, affine, file_name = x
        normalized_image = cv2.normalize(image_data, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        return normalized_image, header, affine, file_name

    normalized_image_rdds = image_rdds.map(normalize_image)
    logger.info("Image normalized successfully!")
    return normalized_image_rdds

# Noice reduction
@task.pyspark(conn_id='NIfTI_Processing')
def denoise_image(image_rdds: RDD):
    def denoise_image(x):
        image_data, header, affine, file_name = x
        denoised_image = cv2.fastNlMeansDenoising(image_data, None, 10, 7, 21)
        return denoised_image, header, affine, file_name

    denoised_image_rdds = image_rdds.map(denoise_image)
    logger.info("Image denoised successfully!")
    return denoised_image_rdds

# Encrypt the image data
@task.pyspark(conn_id='NIfTI_Processing')
def encrypt_image(image_rdds: RDD):
    backend = default_backend()
    salt = b"this is a salt"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(b"123123")
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=backend)

    def encrypt_image_record(record):
        """
        Encrypts a single image record.

        Args:
            record (tuple): A tuple containing (image_data, header, affine, file_name)

        Returns:
            tuple: A tuple containing (encrypted_data, header, affine, file_name)
        """
        image_data, header, affine, file_name = record

        # Generate a unique nonce for AES-CTR
        nonce = os.urandom(16)

        # Initialize Cipher for AES-CTR
        encryptor = cipher.encryptor()

        # Encrypt the image data
        ct = encryptor.update(image_data.tobytes()) + encryptor.finalize()

        # Prepend nonce to ciphertext for use in decryption
        encrypted_data = nonce + ct

        return encrypted_data, header, affine, file_name

    encrypted_image_rdds = image_rdds.map(encrypt_image_record)
    logger.info("Image encrypted successfully!")
    return encrypted_image_rdds
