import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = r"C:\Users\Dell\Downloads\netflix_originals.csv"

df = pd.read_csv(csv_path, encoding="latin1")

df.columns = [c.lower().replace(" ", "_") for c in df.columns]

df["year"] = pd.to_datetime(df["premiere"], errors="coerce").dt.year

df["runtime"] = (
    df["runtime"]
    .astype(str)
    .str.replace(" min", "", regex=False)
    .astype(float)
)

df["imdb_score"] = pd.to_numeric(df["imdb_score"], errors="coerce")

plt.figure(figsize=(8, 5))
df.groupby("year").size().plot(kind="line", marker="o")
plt.title("Number of Netflix Original Films per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
df["imdb_score"].dropna().plot(kind="hist", bins=15, edgecolor="black")
plt.title("Distribution of IMDB Scores")
plt.xlabel("IMDB Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df["runtime"], df["imdb_score"], alpha=0.7)
plt.title("Runtime vs IMDB Score")
plt.xlabel("Runtime (minutes)")
plt.ylabel("IMDB Score")

valid = df[["runtime", "imdb_score"]].dropna()
m, b = np.polyfit(valid["runtime"], valid["imdb_score"], 1)
x = np.linspace(valid["runtime"].min(), valid["runtime"].max(), 100)
plt.plot(x, m * x + b)

plt.grid(True)
plt.tight_layout()
plt.show()

top10 = df.sort_values("imdb_score", ascending=False).head(10)
top10 = top10[["title", "year", "imdb_score", "runtime"]]

fig, ax = plt.subplots(figsize=(10, 3))
ax.axis("off")
ax.set_title("Top 10 Movies Table", fontsize=14, fontweight="bold", pad=20)

table = ax.table(
    cellText=top10.values,
    colLabels=["Title", "Year", "IMDB", "Runtime"],
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(top10.columns))))

plt.tight_layout()
plt.show()
