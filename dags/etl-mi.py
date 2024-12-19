from airflow import DAG
from datetime import datetime
from scripts.extract import download_data, extract_metadata, extract_image_data
from scripts.transform import resize_image, normalize_image, denoise_image, encrypt_image
from scripts.load import load_data

from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 15),
    'retries': 1,
}

with DAG('ETL_MI', default_args=default_args, schedule_interval='@daily') as dag:
    # EXTRACT
    extract_1 = PythonOperator(
        task_id='download',
        python_callable=download_data,
    )
    extract_2 = PythonOperator(
        task_id='extract_metadata',
        python_callable=extract_metadata,
    )

    extract_3 = PythonOperator(
        task_id='extract_image_data',
        python_callable=extract_image_data,
    )
    # TRANSFORM
    transform_1 = PythonOperator(
        task_id='resize_image',
        python_callable=resize_image,
    )
    transform_2 = PythonOperator(
        task_id='normalize_image',
        python_callable=normalize_image,
    )
    transform_3 = PythonOperator(
        task_id='denoise_image',
        python_callable=denoise_image,
    )
    transform_4 = PythonOperator(
        task_id='encrypt_image',
        python_callable=encrypt_image,
    )
    #LOAD
    extract_1 >> extract_2 >> extract_3 >> transform_1 >> transform_2 >> transform_3 >> transform_4