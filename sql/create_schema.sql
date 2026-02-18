-- Drop old tables if they exist (so you can rerun safely)
DROP TABLE IF EXISTS fact_character_scores;
DROP TABLE IF EXISTS fact_material_usage;
DROP TABLE IF EXISTS fact_stats_progression;

DROP TABLE IF EXISTS dim_character;
DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_weapon;
DROP TABLE IF EXISTS dim_vision;

-- DIMENSION TABLES

CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    region VARCHAR(50) UNIQUE
);

CREATE TABLE dim_weapon (
    weapon_id SERIAL PRIMARY KEY,
    weapon_type VARCHAR(50) UNIQUE
);

CREATE TABLE dim_vision (
    vision_id SERIAL PRIMARY KEY,
    vision VARCHAR(50) UNIQUE
);

CREATE TABLE dim_character (
    character_id INT PRIMARY KEY,
    name VARCHAR(100),
    rarity INT,
    region VARCHAR(50),
    vision VARCHAR(50),
    weapon_type VARCHAR(50),
    model VARCHAR(50),
    release_date DATE,
    birthday DATE,
    limited BOOLEAN
);

-- FACT TABLES

CREATE TABLE fact_stats_progression (
    progression_id SERIAL PRIMARY KEY,
    character_id INT,
    level_range VARCHAR(20),
    hp FLOAT,
    atk FLOAT,
    def FLOAT,

    FOREIGN KEY (character_id) REFERENCES dim_character(character_id)
);

CREATE TABLE fact_material_usage (
    usage_id SERIAL PRIMARY KEY,
    character_id INT,
    material_type VARCHAR(50),
    material_name VARCHAR(100),

    FOREIGN KEY (character_id) REFERENCES dim_character(character_id)
);

CREATE TABLE fact_character_scores (
    score_id SERIAL PRIMARY KEY,
    character_id INT,
    hp_growth FLOAT,
    atk_growth FLOAT,
    def_growth FLOAT,
    late_bloomer_index FLOAT,
    bloomANK_type VARCHAR(50),
    meta_efficiency_score FLOAT,

    FOREIGN KEY (character_id) REFERENCES dim_character(character_id)
);

SELECT table_name 
FROM information_schema.tables
WHERE table_schema='public';

SELECT COUNT(*) FROM dim_character;
SELECT COUNT(*) FROM dim_region;
SELECT COUNT(*) FROM dim_weapon;
SELECT COUNT(*) FROM dim_vision;


