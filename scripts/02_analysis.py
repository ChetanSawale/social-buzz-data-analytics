"""
02_analysis.py — Analysis (Social Buzz).

Loads the cleaned modeled dataset and answers the client's questions:
  1. Top 5 content categories by total reaction score.
  2. Monthly trend of reactions (volume + total score).
  3. Breakdown of reactions by content type.
  4. Sentiment distribution of reactions.

Results are saved as CSVs in results/ and key findings are printed.
"""
import pandas as pd

BASE = "/home/hatch/workspace/social-buzz-data-analytics"
CLEANED = f"{BASE}/data/cleaned/social_buzz_cleaned.csv"
RESULTS = f"{BASE}/results"

df = pd.read_csv(CLEANED, parse_dates=["Datetime"])

print("=" * 60)
print("ANALYSIS FINDINGS — Social Buzz")
print("=" * 60)
print(f"Analyzing {len(df):,} cleaned reactions "
      f"across {df['Content ID'].nunique()} content items.\n")

# 1) Top 5 categories by total reaction score
top_cats = (
    df.groupby("Category", as_index=False)["Score"]
    .sum()
    .rename(columns={"Score": "Total Score"})
    .sort_values("Total Score", ascending=False)
    .head(5)
)
top_cats.to_csv(f"{RESULTS}/top5_categories.csv", index=False)
print("1) TOP 5 CATEGORIES BY TOTAL REACTION SCORE")
for _, r in top_cats.iterrows():
    print(f"   {r['Category']:<15} {r['Total Score']:>10,}")
print()

# 2) Monthly trend
df["Month"] = df["Datetime"].dt.to_period("M").astype(str)
monthly = (
    df.groupby("Month", as_index=False)
    .agg(Reactions=("Score", "size"), Total_Score=("Score", "sum"))
)
monthly.to_csv(f"{RESULTS}/monthly_trend.csv", index=False)
peak = monthly.loc[monthly["Total_Score"].idxmax()]
trough = monthly.loc[monthly["Total_Score"].idxmin()]
print("2) MONTHLY TREND")
print(f"   Peak month:   {peak['Month']} ({peak['Reactions']:,} reactions, "
      f"score {peak['Total_Score']:,})")
print(f"   Quiet month:  {trough['Month']} ({trough['Reactions']:,} reactions, "
      f"score {trough['Total_Score']:,})")
print(f"   Avg monthly reactions: {monthly['Reactions'].mean():,.0f}")
print()

# 3) Breakdown by content type
by_type = (
    df.groupby("Content Type", as_index=False)
    .agg(Reactions=("Score", "size"), Total_Score=("Score", "sum"),
         Avg_Score=("Score", "mean"))
    .sort_values("Total_Score", ascending=False)
)
by_type.to_csv(f"{RESULTS}/by_content_type.csv", index=False)
print("3) BREAKDOWN BY CONTENT TYPE")
for _, r in by_type.iterrows():
    print(f"   {r['Content Type']:<8} {r['Reactions']:>6,} reactions | "
          f"total score {r['Total_Score']:>8,} | avg score {r['Avg_Score']:.1f}")
print()

# 4) Sentiment distribution
sentiment = (
    df.groupby("Sentiment", as_index=False)
    .agg(Reactions=("Score", "size"), Total_Score=("Score", "sum"))
)
sentiment["Share %"] = (sentiment["Reactions"] / sentiment["Reactions"].sum() * 100).round(1)
sentiment = sentiment.sort_values("Reactions", ascending=False)
sentiment.to_csv(f"{RESULTS}/sentiment_distribution.csv", index=False)
print("4) SENTIMENT DISTRIBUTION")
for _, r in sentiment.iterrows():
    print(f"   {r['Sentiment']:<10} {r['Reactions']:>6,} reactions ({r['Share %']}%)")
print("=" * 60)
print(f"CSVs saved to: {RESULTS}/")
