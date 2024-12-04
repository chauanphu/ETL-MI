import kagglehub

# Download latest version
path = kagglehub.dataset_download("andrewmvd/covid19-ct-scans")

print("Path to dataset files:", path)