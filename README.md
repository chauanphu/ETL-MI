# ETL for Medical Image

## Project Folder

```
medical_image_etl/
│
├── data/
│   ├── raw/
│   │   ├── images/
│   │   │   └── *.png / *.dcm / other image formats
│   │   └── metadata/
│   │       └── metadata.csv
│   │
│   ├── processed/
│   │   ├── images/
│   │   │   └── *.png / *.parquet / other processed formats
│   │   └── metadata/
│   │       └── processed_metadata.parquet
│   │
│   └── interim/
│       └── temporary files during ETL
│
├── scripts/
│   ├── extract/
│   │   ├── download_data.py
│   │   └── upload_to_storage.py
│   │
│   ├── transform/
│   │   ├── preprocess_images.py
│   │   ├── process_metadata.py
│   │   └── integrate_data.py
│   │
│   └── load/
│       ├── load_to_s3.py
│       └── load_to_redshift.py
│
├── config/
│   ├── config.yaml
│   └── credentials.yaml
│
├── pipelines/
│   ├── airflow_dags/
│   │   └── medical_image_etl_dag.py
│   └── spark_jobs/
│       ├── preprocess_images_job.py
│       └── transform_metadata_job.py
│
├── logs/
│   ├── extract/
│   ├── transform/
│   └── load/
│
├── tests/
│   ├── unit/
│   │   ├── test_download_data.py
│   │   └── test_preprocess_images.py
│   └── integration/
│       └── test_full_pipeline.py
│
├── docs/
│   ├── architecture_diagram.png
│   ├── pipeline_overview.md
│   └── data_dictionary.md
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── data_validation.ipynb
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```