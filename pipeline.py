from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
from scripts import extract, transform, load

default_args = {
    'owner': 'Châu An Phú',
    'start_date': datetime(2024, 12, 6),
    'retries': 1,
}

def encrypt_files():
    # Your existing encryption logic
    pass

def upload_to_minio():
    # Your existing upload logic
    pass

with DAG('etl_pipeline', default_args=default_args, schedule_interval=None) as dag:
    download_task = PythonOperator(
        task_id='download_kaggle_data',
        python_callable=extract.download_data
    )
    
    process_task = PythonOperator(
        task_id='process_nifti_files',
        python_callable=transform.process_nifti_files
    )
    
    encrypt_task = PythonOperator(
        task_id='encrypt_files',
        python_callable=encrypt_files
    )
    
    upload_task = PythonOperator(
        task_id='upload_to_minio',
        python_callable=upload_to_minio
    )
    
    # Define task dependencies
    download_task >> process_task >> encrypt_task >> upload_task
