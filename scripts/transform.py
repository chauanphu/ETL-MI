import numpy as np
from pyspark.sql import SparkSession
import os
import nibabel as nib

def process_nifti_files():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("NIfTI_Processing") \
        .getOrCreate()
    
    nifti_dir = '/tmp/ct_scan_data'
    nifti_files = [os.path.join(nifti_dir, f) for f in os.listdir(nifti_dir) if f.endswith('.nii')]
    nifti_rdd = spark.sparkContext.parallelize(nifti_files)
    
    def compute_mean(file_path):
        try:
            nii_img = nib.load(file_path)
            data = nii_img.get_fdata()
            mean = np.mean(data)
            return (file_path, mean)
        except Exception as e:
            return (file_path, str(e))
    
    results = nifti_rdd.map(compute_mean).collect()
    
    # Optionally, store results somewhere
    with open('/tmp/processing_results.txt', 'w') as f:
        for file, mean in results:
            f.write(f"{file}: {mean}\n")
    
    spark.stop()