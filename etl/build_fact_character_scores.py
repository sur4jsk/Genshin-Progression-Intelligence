import pandas as pd

df = pd.read_csv("data/processed/cleaned_genshin.csv")

# Fix column name issue if still present
if "__character_name" in df.columns:
    df.rename(columns={"__character_name": "character_name"}, inplace=True)

df = df.reset_index(drop=True)
df["character_id"] = df.index + 1

# Use Level 1-20 and Level 90-90 for growth comparison
df["hp_growth"] = (df["hp_90_90"] - df["hp_1_20"]) / df["hp_1_20"]
df["atk_growth"] = (df["atk_90_90"] - df["atk_1_20"]) / df["atk_1_20"]
df["def_growth"] = (df["def_90_90"] - df["def_1_20"]) / df["def_1_20"]

# Late Bloomer Index: how much ATK grows relative to HP
df["late_bloomer_index"] = df["atk_growth"] / (df["hp_growth"] + 0.001)

def bloom_label(x):
    if x > 1.15:
        return "Late Bloomer"
    elif x < 0.85:
        return "Early Carry"
    else:
        return "Balanced"

df["bloom_type"] = df["late_bloomer_index"].apply(bloom_label)

# Meta Efficiency Score (weighted power score)
df["meta_efficiency_score"] = (
    df["atk_90_90"] * 0.50 +
    df["hp_90_90"] * 0.20 +
    df["def_90_90"] * 0.30
)

scores = df[[
    "character_id",
    "hp_growth",
    "atk_growth",
    "def_growth",
    "late_bloomer_index",
    "bloom_type",
    "meta_efficiency_score"
]]

scores.to_csv("data/processed/fact_character_scores.csv", index=False)

print("✅ fact_character_scores.csv created successfully!")
print("Rows:", len(scores))
print(scores.head())
