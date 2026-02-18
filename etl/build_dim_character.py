import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/cleaned_genshin.csv")
OUT_PATH = Path("data/processed/dim_character.csv")

df = pd.read_csv(IN_PATH)

# make sure the column name is correct
# if your cleaned file uses "__character_name" you already renamed it earlier
required = {"character_id", "character_name", "rarity", "vision", "weapon_type",
            "region", "model", "release_date", "birthday", "limited"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in cleaned_genshin.csv: {missing}")

dim = (
    df[list(required)]
    .drop_duplicates(subset=["character_id"])
    .sort_values("character_id")
)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
dim.to_csv(OUT_PATH, index=False)

print(f"✅ Rebuilt {OUT_PATH} with character_name ({len(dim)} rows)")
