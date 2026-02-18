import pandas as pd
import os

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_genshin.csv")

# Ensure output folder exists
os.makedirs("data/processed", exist_ok=True)

# Add character_id
df = df.reset_index(drop=True)
df["character_id"] = df.index + 1

# -----------------------------
# DIM CHARACTER
# -----------------------------
dim_character_cols = [col for col in [
    "character_id",
    "name",
    "rarity",
    "vision",
    "weapon_type",
    "region",
    "model",
    "release_date",
    "birthday",
    "limited"
] if col in df.columns]

dim_character = df[dim_character_cols]
dim_character.to_csv("data/processed/dim_character.csv", index=False)
print("✅ dim_character created")

# -----------------------------
# DIM REGION
# -----------------------------
if "region" in df.columns:
    dim_region = df[["region"]].drop_duplicates().reset_index(drop=True)
    dim_region["region_id"] = dim_region.index + 1
    dim_region = dim_region[["region_id", "region"]]
    dim_region.to_csv("data/processed/dim_region.csv", index=False)
    print("✅ dim_region created")
else:
    print("❌ region column not found in dataset")

# -----------------------------
# DIM WEAPON
# -----------------------------
if "weapon_type" in df.columns:
    dim_weapon = df[["weapon_type"]].drop_duplicates().reset_index(drop=True)
    dim_weapon["weapon_id"] = dim_weapon.index + 1
    dim_weapon = dim_weapon[["weapon_id", "weapon_type"]]
    dim_weapon.to_csv("data/processed/dim_weapon.csv", index=False)
    print("✅ dim_weapon created")
else:
    print("❌ weapon_type column not found in dataset")

# -----------------------------
# DIM VISION
# -----------------------------
if "vision" in df.columns:
    dim_vision = df[["vision"]].drop_duplicates().reset_index(drop=True)
    dim_vision["vision_id"] = dim_vision.index + 1
    dim_vision = dim_vision[["vision_id", "vision"]]
    dim_vision.to_csv("data/processed/dim_vision.csv", index=False)
    print("✅ dim_vision created")
else:
    print("❌ vision column not found in dataset")
