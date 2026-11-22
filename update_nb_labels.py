import json

with open("notebooks/final_notebook.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "sns.heatmap" in source:
            old_str = 'plt.title("Entity Co-occurrence Heatmap across Clinical Corpus", fontsize=12, fontweight="bold")'
            new_str = (
                'plt.title("Entity Co-occurrence Heatmap across Clinical Corpus", fontsize=12, fontweight="bold", pad=12)\n'
                'plt.xlabel("Target Entity Category", fontsize=10, fontweight="bold", labelpad=8)\n'
                'plt.ylabel("Source Entity Category", fontsize=10, fontweight="bold", labelpad=8)'
            )
            if old_str in source:
                source = source.replace(old_str, new_str)
                lines = source.split("\n")
                cell["source"] = [line + "\n" for line in lines[:-1]] + [lines[-1]]
                print(f"Cell {i+1} updated with X and Y labels!")

with open("notebooks/final_notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

# Also copy to round2_modeling_pipeline.ipynb
with open("round2_modeling_pipeline.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Saved notebooks/final_notebook.ipynb and round2_modeling_pipeline.ipynb")
