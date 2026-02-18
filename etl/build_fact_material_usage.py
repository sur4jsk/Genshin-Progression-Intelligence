import pandas as pd

df = pd.read_csv("data/processed/cleaned_genshin.csv")
df = df.reset_index(drop=True)
df["character_id"] = df.index + 1

material_cols = [col for col in df.columns if "material" in col or "talent" in col or "book" in col]

records = []

for _, row in df.iterrows():
    for col in material_cols:
        value = row[col]
        if pd.notna(value):
            records.append({
                "character_id": row["character_id"],
                "material_type": col,
                "material_name": value
            })

fact_material = pd.DataFrame(records)
fact_material.to_csv("data/processed/fact_material_usage.csv", index=False)
print("fact_material_usage created")
