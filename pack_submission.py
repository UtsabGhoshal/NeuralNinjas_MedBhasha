import zipfile
import os
import shutil

zip_name = "NeuralNinjas_MedBhasha.zip"
temp_zip = "NeuralNinjas_MedBhasha_new.zip"

files_to_pack = [
    'README.md',
    'notebooks/final_notebook.ipynb',
    'predictions/ner_predictions.csv',
    'predictions/clusters.csv',
    'predictions/analysis/cluster_distribution.png',
    'predictions/analysis/entity_frequency.png',
    'predictions/analysis/entity_cooccurrence_heatmap.png',
    'predictions/analysis/entity_frequencies.csv',
    'predictions/analysis/entity_cooccurrence_matrix.csv',
    'predictions/rag_outputs.jsonl',
    'data/annotated_corpus.csv',
    'raw_data.csv',
    'validation_report.txt',
    'source_declaration.md',
    'eda_summary.pdf',
    'requirements.txt',
    'report.pdf'
]

print("Packing files into zip...")
with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_pack:
        if not os.path.exists(f):
            raise FileNotFoundError(f"Missing required file: {f}")
        zf.write(f, f)
        print(f"  + {f} ({os.path.getsize(f):,} bytes)")

if os.path.exists(zip_name):
    os.remove(zip_name)
shutil.move(temp_zip, zip_name)

print(f"\nFinal archive created successfully at: {zip_name} ({os.path.getsize(zip_name):,} bytes)")
