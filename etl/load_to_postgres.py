import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection Details
DB_USER = "postgres"
DB_PASSWORD = "0zzyM%40n2004"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "genshin_dw"

# Create connection engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("✅ Connected to PostgreSQL successfully")
from sqlalchemy import text

# Clear tables before loading to avoid duplicates
with engine.begin() as conn:
    conn.execute(text("""
    TRUNCATE TABLE
        fact_character_scores,
        fact_stats_progression,
        dim_character,
        dim_region,
        dim_weapon,
        dim_vision
    RESTART IDENTITY CASCADE;
    """))
print("🧹 Tables cleared before loading")

# Load CSV files into tables
tables = {
    "dim_character": "data/processed/dim_character.csv",
    "dim_region": "data/processed/dim_region.csv",
    "dim_weapon": "data/processed/dim_weapon.csv",
    "dim_vision": "data/processed/dim_vision.csv",
    "fact_stats_progression": "data/processed/fact_stats_progression.csv",
    "fact_character_scores": "data/processed/fact_character_scores.csv",
    # Add fact tables later once created
    # "fact_stats_progression": "data/processed/fact_stats_progression.csv",
    # "fact_material_usage": "data/processed/fact_material_usage.csv",
    # "fact_character_scores": "data/processed/fact_character_scores.csv"
}

for table_name, file_path in tables.items():
    print(f"\n📌 Loading {file_path} into {table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(table_name, engine, if_exists="append", index=False)

    print(f"✅ Loaded {len(df)} rows into {table_name}")

print("\n🎉 All dimension tables loaded successfully!")

