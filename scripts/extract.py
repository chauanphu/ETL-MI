import os
import kagglehub

os.makedirs("rawdata", exist_ok=True)

def download_data():
    # Download latest version to rawdata folder
    path = kagglehub.dataset_download("andrewmvd/covid19-ct-scans", path="rawdata")
    print("Path to dataset files:", path)