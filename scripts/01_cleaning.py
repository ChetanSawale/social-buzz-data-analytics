"""
01_cleaning.py — Data cleaning & data modeling (Social Buzz).

Steps (with Excel/Power BI equivalents):
  1. Load the three raw CSVs.
  2. Remove rows with missing values (like Excel "Go To Special > Blanks" + delete).
  3. Drop irrelevant columns: URL (Content), Platform (Reactions).
  4. Fix data types: Datetime -> datetime64 (like Excel "Text to Columns" / Power Query type change);
     drop rows whose Datetime cannot be parsed.
  5. Merge the three tables on Content ID / Reaction Type  (pandas merge ≈ Excel VLOOKUP / Power BI relationships).
  6. Compute total reaction score per content item (groupby + sum ≈ Excel SUMIF / Power BI SUMX measure).
  7. Save the modeled table to data/cleaned/social_buzz_cleaned.csv and print a cleaning summary.
"""
import pandas as pd

RAW = "/home/hatch/workspace/social-buzz-data-analytics/data/raw"
OUT = "/home/hatch/workspace/social-buzz-data-analytics/data/cleaned/social_buzz_cleaned.csv"

content = pd.read_csv(f"{RAW}/Content.csv")
reactions = pd.read_csv(f"{RAW}/Reactions.csv")
reaction_types = pd.read_csv(f"{RAW}/ReactionTypes.csv")

rows_before = {"Content": len(content), "Reactions": len(reactions)}

# 1) Drop irrelevant columns
content = content.drop(columns=["URL"])
reactions = reactions.drop(columns=["Platform"])

# 2) Fix data types — Datetime to datetime; unparseable -> NaT
reactions["Datetime"] = pd.to_datetime(reactions["Datetime"], errors="coerce")

# 3) Remove rows with missing values
nulls_before = int(content.isna().sum().sum() + reactions.isna().sum().sum())
content = content.dropna()
reactions = reactions.dropna()

rows_after = {"Content": len(content), "Reactions": len(reactions)}

# 4) Merge (modeling): reactions + content on Content ID, then + reaction metadata on Reaction Type
merged = reactions.merge(content, on="Content ID", how="inner")
merged = merged.merge(reaction_types, on="Reaction Type", how="inner")

# 5) Total reaction score per content item  (≈ SUMIF over Score by Content ID)
content_score = (
    merged.groupby(["Content ID", "Content Type", "Category"], as_index=False)["Score"]
    .sum()
    .rename(columns={"Score": "Total Score"})
)

merged.to_csv(OUT, index=False)
content_score.to_csv(
    "/home/hatch/workspace/social-buzz-data-analytics/results/content_scores.csv",
    index=False,
)

print("=" * 60)
print("CLEANING SUMMARY — Social Buzz")
print("=" * 60)
print(f"Content rows:   {rows_before['Content']} -> {rows_after['Content']} "
      f"({rows_before['Content'] - rows_after['Content']} removed)")
print(f"Reaction rows:  {rows_before['Reactions']} -> {rows_after['Reactions']} "
      f"({rows_before['Reactions'] - rows_after['Reactions']} removed)")
print(f"Null / unparseable values removed: {nulls_before}")
print(f"Merged rows (reactions x content x reaction types): {len(merged)}")
print(f"Unique content items scored: {len(content_score)}")
print(f"Dropped columns: URL (Content), Platform (Reactions)")
print(f"Datetime dtype: {merged['Datetime'].dtype}")
print(f"Cleaned dataset saved to: {OUT}")
print("=" * 60)
