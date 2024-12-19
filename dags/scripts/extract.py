import os
from typing import List
import kagglehub
import pandas as pd
from airflow.decorators import task
import logging
import nibabel as nib
import numpy as np
from pyspark import RDD, SparkContext
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = "../rawdata/"

# @task.pyspark(conn_id='NIfTI_Processing')
def download_data():
    if os.path.exists(OUTPUT_DIR):
        return
    os.makedirs("OUTPUT_DIR", exist_ok=True)
    # Download latest version to rawdata folder
    path = kagglehub.dataset_download("andrewmvd/covid19-ct-scans")
    print("Path to dataset files:", path)
    # Move the downloaded folder to the rawdata directory, For example: 4/ct_scans, 4/metadata -> rawdata/ct_scans, rawdata/metadata
    os.rename(path, OUTPUT_DIR)
    print("Data downloaded and unzipped successfully!")


def rename_data_folder():
    # Extract metadata from the downloaded dataset
    metadata = pd.read_csv(f"{OUTPUT_DIR}/metadata.csv")
    logger.info("Metadata extracted successfully!")
    metadata.replace("../input/covid19-ct-scans/", OUTPUT_DIR, regex=True, inplace=True)
    image_paths = metadata.to_numpy()
    image_paths = image_paths.flatten()
    return image_paths

def extract_metadata():
    # Extract metadata from the downloaded dataset
    path = os.path.join(OUTPUT_DIR, "metadata.csv")
    metadata = pd.read_csv(path)
    logger.info("Metadata extracted successfully!")
    metadata.replace("../input/covid19-ct-scans/", "", regex=True, inplace=True)
    return metadata

@task.pyspark(conn_id='NIfTI_Processing')
def extract_image_data(spark: SparkSession, sc: SparkContext, metadata: pd.DataFrame) -> RDD:
    # Convert DataFrame to np array
    image_paths: np.ndarray = metadata.to_numpy().flatten()
    # Extract image data
    def load_image(x):
        path = os.path.join(OUTPUT_DIR, x)
        nifti_data = nib.load(path)
        header = nifti_data.header
        affine = nifti_data.affine
        image_data = nifti_data.get_fdata()
        image_data = np.array(image_data)

        return image_data, header, affine, x

    image_rdds = sc.parallelize(image_paths).map(load_image)

    return image_rdds

if __name__ == "__main__":
    download_data()
    metadata = rename_data_folder()
    extract_image_data(metadata)