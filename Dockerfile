FROM apache/airflow:slim-2.10.4rc1-python3.12

# Install additional OS packages if needed
USER root
RUN apt-get update && apt-get install -y \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install additional Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


