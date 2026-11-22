# -*- coding: utf-8 -*-
"""
Regenerate Analysis Plots with Explicit Titles, X-Labels, and Y-Labels.
Includes NotoSansBengali font registration and English labels per official guidance.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# Register NotoSansBengali font for matplotlib
font_path = "NotoSansBengali-Regular.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Noto Sans Bengali', 'DejaVu Sans', 'Arial']

sns.set_theme(style="whitegrid")
os.makedirs("predictions/analysis", exist_ok=True)
os.makedirs("output/eda_charts", exist_ok=True)

# 1. Regenerate predictions/analysis/ plots
clusters_df = pd.read_csv("predictions/clusters.csv")
ner_df = pd.read_csv("predictions/ner_predictions.csv")

# Chart 1: Cluster Distribution
plt.figure(figsize=(9, 4.5))
cluster_counts = clusters_df["cluster_id"].value_counts().sort_index()
bars = plt.bar(cluster_counts.index, cluster_counts.values, color=sns.color_palette("viridis", len(cluster_counts)))
plt.title("Phenotype Cluster Distribution across Test Notes (k=12)", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Phenotype Cluster ID", fontsize=11, fontweight="bold")
plt.ylabel("Number of Clinical Notes", fontsize=11, fontweight="bold")
plt.xticks(cluster_counts.index)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 3, f"{int(yval)}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("predictions/analysis/cluster_distribution.png", dpi=250)
plt.close()
print("Saved predictions/analysis/cluster_distribution.png with clear title, X and Y labels.")

# Chart 2: Predicted Entity Frequency Distribution
plt.figure(figsize=(8.5, 5))
ent_counts = ner_df["entity_type"].value_counts()
palette = sns.color_palette("mako", len(ent_counts))
bars = plt.barh(ent_counts.index, ent_counts.values, color=palette)
plt.title("Extracted Clinical Entity Frequency Distribution (Test Data)", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Total Extracted Entity Spans", fontsize=11, fontweight="bold")
plt.ylabel("Entity Category", fontsize=11, fontweight="bold")
plt.gca().invert_yaxis()
for bar in bars:
    w = bar.get_width()
    plt.text(w + 100, bar.get_y() + bar.get_height()/2, f"{int(w):,}", va="center", ha="left", fontsize=9)
plt.tight_layout()
plt.savefig("predictions/analysis/entity_frequency.png", dpi=250)
plt.close()
print("Saved predictions/analysis/entity_frequency.png with clear title, X and Y labels.")

# Chart 3: Entity Co-occurrence Matrix
schema_types = ['DIAGNOSIS', 'SYMPTOM', 'MEDICATION', 'DOSAGE', 'TEST', 'TEST_RESULT', 'BODY_SITE', 'PROCEDURE', 'TEMPORAL', 'NEGATION_UNCERTAINTY']
co_df = pd.read_csv("predictions/analysis/entity_cooccurrence_matrix.csv", index_col=0)

plt.figure(figsize=(9, 7.5))
sns.heatmap(co_df, annot=True, fmt=".0f", xticklabels=schema_types, yticklabels=schema_types, cmap="Blues", cbar=True)
plt.title("Clinical Entity Co-occurrence Matrix (Test Data)", fontsize=13, fontweight="bold", pad=14)
plt.xlabel("Target Entity Category", fontsize=11, fontweight="bold", labelpad=8)
plt.ylabel("Source Entity Category", fontsize=11, fontweight="bold", labelpad=8)
plt.xticks(rotation=45, ha='right', fontsize=9.5)
plt.yticks(fontsize=9.5)
plt.tight_layout()
plt.savefig("predictions/analysis/entity_cooccurrence_heatmap.png", dpi=250)
plt.close()
print("Saved predictions/analysis/entity_cooccurrence_heatmap.png with clear title, X and Y labels.")

# 2. Regenerate output/eda_charts/ cooccurrence_heatmap.png with explicit X and Y labels
from pipeline.generate_eda import analyze_corpus, generate_charts, build_pdf
stats = analyze_corpus("output/annotated_corpus.csv")
chart1, chart2, chart3 = generate_charts(stats, "output/eda_charts")

# Also ensure chart3 (cooccurrence_heatmap) in eda_charts has explicit labels
plt.figure(figsize=(8.5, 7))
etypes = stats["all_entity_types"]
matrix_vals = np.zeros((len(etypes), len(etypes)))
for i, e1 in enumerate(etypes):
    for j, e2 in enumerate(etypes):
        matrix_vals[i, j] = stats["co_matrix"][e1][e2]
sns.heatmap(matrix_vals, annot=True, fmt=".0f", xticklabels=etypes, yticklabels=etypes, cmap="YlGnBu", cbar=True)
plt.title("Entity Co-occurrence Matrix Across Clinical Notes", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Target Entity Category", fontsize=11, fontweight="bold", labelpad=8)
plt.ylabel("Source Entity Category", fontsize=11, fontweight="bold", labelpad=8)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(fontsize=9)
plt.tight_layout()
plt.savefig("output/eda_charts/cooccurrence_heatmap.png", dpi=250)
plt.close()

# Rebuild eda_summary.pdf
build_pdf(stats, (chart1, chart2, "output/eda_charts/cooccurrence_heatmap.png"), "output/eda_summary.pdf")
import shutil
shutil.copyfile("output/eda_summary.pdf", "eda_summary.pdf")
print("Updated eda_summary.pdf successfully!")
