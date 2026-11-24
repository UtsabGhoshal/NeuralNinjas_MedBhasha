import json
import os

with open("notebooks/final_notebook.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "def load_corpus" in source:
            old_code = 'def load_corpus(csv_path="output/annotated_corpus.csv"):'
            new_code = '''def load_corpus(csv_path=None):
    if csv_path is None:
        candidates = [
            "data/annotated_corpus.csv",
            "../data/annotated_corpus.csv",
            "output/annotated_corpus.csv",
            "../output/annotated_corpus.csv"
        ]
        for p in candidates:
            if os.path.exists(p):
                csv_path = p
                break
    if csv_path is None or not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find annotated_corpus.csv in data/ or output/")'''
            source = source.replace(old_code, new_code)
            source = source.replace('load_corpus("output/annotated_corpus.csv")', 'load_corpus()')
            lines = source.split("\n")
            cell["source"] = [l + "\n" for l in lines[:-1]] + [lines[-1]]
            print(f"Cell {i+1} robust path updated!")

with open("notebooks/final_notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

with open("round2_modeling_pipeline.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Updated both notebooks successfully!")
