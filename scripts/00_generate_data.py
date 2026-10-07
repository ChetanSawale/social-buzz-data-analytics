"""
Generate synthetic Social Buzz datasets for portfolio purposes.
This data is SIMULATED — it mimics the structure of the Accenture Forage
"Data Analytics and Visualization" job simulation (fictional client: Social Buzz).
No real user data is used.
"""
import random
import pandas as pd

random.seed(42)

BASE = "/home/hatch/workspace/social-buzz-data-analytics/data/raw"

# ---------------- Content.csv (~500 rows) ----------------
content_types = ["photo", "video", "GIF", "audio"]
categories = ["Animals", "Science", "Healthy Eating", "Technology", "Food",
              "Travel", "Fitness", "Education", "Culture", "Sports"]

content_ids = [f"C{i:04d}" for i in range(1, 501)]
contents = []
for cid in content_ids:
    contents.append({
        "Content ID": cid,
        "Content Type": random.choice(content_types),
        "Category": random.choices(categories, weights=[15, 10, 12, 10, 13, 9, 8, 9, 7, 7])[0],
        "URL": f"https://socialbuzz.example.com/content/{cid.lower()}",
    })
content_df = pd.DataFrame(contents)

# Inject a few dirty rows to demonstrate cleaning (~2% missing category, ~1% missing type)
for idx in random.sample(range(len(content_df)), 10):
    content_df.loc[idx, "Category"] = None
for idx in random.sample(range(len(content_df)), 5):
    content_df.loc[idx, "Content Type"] = None
content_df.to_csv(f"{BASE}/Content.csv", index=False)

# ---------------- Reactions.csv (~5000 rows) ----------------
reaction_types = ["heart", "want", "disgust", "hate", "interested",
                  "indifferent", "love", "super love", "cherish", "adore",
                  "like", "dislike", "intrigued", "peeking", "scared"]
user_ids = [f"U{i:05d}" for i in range(1, 2001)]

# Weight content so some posts are viral (realistic skew)
viral = random.sample(content_ids, 40)
weights = [8 if c in viral else 1 for c in content_ids]

reactions = []
start = pd.Timestamp("2024-01-01")
end = pd.Timestamp("2024-12-31")
for _ in range(5000):
    cid = random.choices(content_ids, weights=weights)[0]
    dt = start + pd.Timedelta(days=random.randint(0, (end - start).days),
                              hours=random.randint(0, 23),
                              minutes=random.randint(0, 59))
    reactions.append({
        "Content ID": cid,
        "User ID": random.choice(user_ids),
        "Reaction Type": random.choice(reaction_types),
        "Datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        # Irrelevant column to demonstrate dropping
        "Platform": random.choice(["web", "ios", "android"]),
    })
reactions_df = pd.DataFrame(reactions)

# Inject dirty rows (~2% missing reaction type, a few bad datetimes)
for idx in random.sample(range(len(reactions_df)), 100):
    reactions_df.loc[idx, "Reaction Type"] = None
bad_idx = random.sample(range(len(reactions_df)), 8)
reactions_df.loc[bad_idx, "Datetime"] = "not-a-date"
reactions_df.to_csv(f"{BASE}/Reactions.csv", index=False)

# ---------------- ReactionTypes.csv ----------------
reaction_meta = [
    ("heart", "positive", 60), ("want", "positive", 70), ("disgust", "negative", 0),
    ("hate", "negative", 5), ("interested", "positive", 30), ("indifferent", "neutral", 20),
    ("love", "positive", 65), ("super love", "positive", 75), ("cherish", "positive", 70),
    ("adore", "positive", 72), ("like", "positive", 50), ("dislike", "negative", 10),
    ("intrigued", "positive", 45), ("peeking", "neutral", 35), ("scared", "negative", 15),
]
rt_df = pd.DataFrame(reaction_meta, columns=["Reaction Type", "Sentiment", "Score"])
rt_df.to_csv(f"{BASE}/ReactionTypes.csv", index=False)

print(f"Content.csv:   {len(content_df)} rows")
print(f"Reactions.csv: {len(reactions_df)} rows")
print(f"ReactionTypes.csv: {len(rt_df)} rows")
print("Synthetic data generated in", BASE)
