import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_genshin.csv")

# Fix column name issue (if still exists)
if "__character_name" in df.columns:
    df.rename(columns={"__character_name": "character_name"}, inplace=True)

# Add character_id
df = df.reset_index(drop=True)
df["character_id"] = df.index + 1

# Level ranges based on your dataset columns
level_ranges = [
    "1_20", "20_20", "20_40", "40_40", "40_50",
    "50_50", "50_60", "60_60", "60_70",
    "70_70", "70_80", "80_80", "80_90", "90_90"
]

rows = []

for _, row in df.iterrows():
    cid = row["character_id"]

    for lvl in level_ranges:
        hp_col = f"hp_{lvl}"
        atk_col = f"atk_{lvl}"
        def_col = f"def_{lvl}"

        # Only add row if those columns exist
        if hp_col in df.columns and atk_col in df.columns and def_col in df.columns:
            rows.append({
                "character_id": cid,
                "level_range": lvl.replace("_", "-"),
                "hp": row[hp_col],
                "atk": row[atk_col],
                "def": row[def_col]
            })

fact_stats = pd.DataFrame(rows)

# Save output
fact_stats.to_csv("data/processed/fact_stats_progression.csv", index=False)

print("✅ fact_stats_progression.csv created successfully!")
print("Rows created:", len(fact_stats))
print(fact_stats.head())
