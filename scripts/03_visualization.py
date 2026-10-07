"""
03_visualization.py — Dashboard charts (Social Buzz).

Reads results/*.csv and renders clean, labeled PNG charts into dashboard/
(matplotlib/seaborn ≈ Power BI visuals).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")
BASE = "/home/hatch/workspace/social-buzz-data-analytics"
DASH = f"{BASE}/dashboard"

# 1) Top 5 categories — horizontal bar
top5 = pd.read_csv(f"{BASE}/results/top5_categories.csv")
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=top5, x="Total Score", y="Category", palette="viridis", ax=ax)
ax.set_title("Top 5 Content Categories by Total Reaction Score", fontsize=14, weight="bold")
ax.set_xlabel("Total Reaction Score")
ax.set_ylabel("Category")
for i, v in enumerate(top5["Total Score"]):
    ax.text(v + 300, i, f"{v:,}", va="center", fontsize=10)
fig.tight_layout()
fig.savefig(f"{DASH}/top5_categories.png", dpi=150)
plt.close(fig)

# 2) Monthly trend — line chart
monthly = pd.read_csv(f"{BASE}/results/monthly_trend.csv")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["Month"], monthly["Total_Score"], marker="o", linewidth=2, color="#1f77b4")
ax.fill_between(monthly["Month"], monthly["Total_Score"], alpha=0.15, color="#1f77b4")
ax.set_title("Monthly Reaction Score Trend (2024)", fontsize=14, weight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Total Reaction Score")
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()
fig.savefig(f"{DASH}/monthly_trend.png", dpi=150)
plt.close(fig)

# 3) Content type breakdown — bar
by_type = pd.read_csv(f"{BASE}/results/by_content_type.csv")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=by_type, x="Content Type", y="Total_Score", palette="magma", ax=ax)
ax.set_title("Total Reaction Score by Content Type", fontsize=14, weight="bold")
ax.set_xlabel("Content Type")
ax.set_ylabel("Total Reaction Score")
for i, v in enumerate(by_type["Total_Score"]):
    ax.text(i, v + 600, f"{v:,}", ha="center", fontsize=10)
fig.tight_layout()
fig.savefig(f"{DASH}/content_type_breakdown.png", dpi=150)
plt.close(fig)

# 4) Sentiment distribution — donut
sent = pd.read_csv(f"{BASE}/results/sentiment_distribution.csv")
fig, ax = plt.subplots(figsize=(7, 5))
colors = {"positive": "#2ca02c", "negative": "#d62728", "neutral": "#7f7f7f"}
wedges, texts, autotexts = ax.pie(
    sent["Reactions"], labels=sent["Sentiment"],
    colors=[colors[s] for s in sent["Sentiment"]],
    autopct=lambda p: f"{p:.1f}%",
    startangle=90, wedgeprops=dict(width=0.45, edgecolor="white"),
)
ax.set_title("Reaction Sentiment Distribution", fontsize=14, weight="bold")
fig.tight_layout()
fig.savefig(f"{DASH}/sentiment_donut.png", dpi=150)
plt.close(fig)

print("Charts saved to", DASH)
import os
for f in sorted(os.listdir(DASH)):
    print(" -", f, f"{os.path.getsize(DASH + '/' + f) // 1024} KB")
