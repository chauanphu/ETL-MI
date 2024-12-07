import os
import kagglehub
from airflow.decorators import task

@task.pyspark(conn_id='NIfTI_Processing')
def download_data():
    os.makedirs("rawdata", exist_ok=True)
    # Download latest version to rawdata folder
    path = kagglehub.dataset_download("andrewmvd/covid19-ct-scans", path="rawdata")
    print("Path to dataset files:", path)

if __name__ == "__main__":
    download_data()