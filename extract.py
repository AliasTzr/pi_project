import zipfile, os

zip_path = "dataset/dataset.zip"
    # Décompresser le fichier ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('dataset')
print(os.path.join("dataset", "dataset.csv"))
os.remove("dataset/dataset.csv")