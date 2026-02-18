import pandas as pd

stats = pd.read_csv("data/processed/fact_stats_progression.csv")

#extract stats at level1 and level90
lvl1 = stats[stats["level_range"] == "1-20"]
lvl60 = stats[stats["level_range"] == "50-60"]
lvl90 = stats[stats["level_range"] == "90-90"]

#merge level values
merged = lvl1.merge(lvl60, on="character_id", suffixes=("_lvl1", "_lvl60"))
merged = merged.merge(lvl90, on="character_id")
merged = merged.rename(columns={
    "hp": "hp_lvl90",
    "atk": "atk_lvl90",
    "def": "def_lvl90"
})

#growth rate calculation
merged["atk_growth"] = (merged["atk_lvl90"] - merged["atk_lvl1"]) / merged["atk_lvl1"]
merged["hp_growth"] = (merged["hp_lvl90"] - merged["hp_lvl1"]) / merged["hp_lvl1"]
merged["def_growth"] = (merged["def_lvl90"] - merged["def_lvl1"]) / merged["def_lvl1"]

#late bloomer index
merged["atk_early_gain"] = merged["atk_lvl60"] - merged["atk_lvl1"]
merged["atk_late_gain"] = merged["atk_lvl90"] - merged["atk_lvl60"]

merged["late_bloomer_index"] = merged["atk_late_gain"] / (merged["atk_early_gain"] + 0.0001)

#bloom type classifaction
def classify_bloom(x):
    if x > 1.2:
        return "Late Bloomer"
    elif x < 0.8:
        return "Early Carry"
    else:
        return "Balanced"

merged["bloom_type"] = merged["late_bloomer_index"].apply(classify_bloom)

#meta efficiency score 
merged["meta_efficiency_score"] = (
    merged["atk_lvl90"] * 0.5 +
    merged["hp_lvl90"] * 0.2 +
    merged["def_lvl90"] * 0.3
)

#save fact_character_scores 
final_scores = merged[[
    "character_id",
    "atk_growth",
    "hp_growth",
    "def_growth",
    "late_bloomer_index",
    "bloom_type",
    "meta_efficiency_score"
]]

final_scores.to_csv("data/processed/fact_character_scores.csv", index=False)
print("fact_character_scores created")

