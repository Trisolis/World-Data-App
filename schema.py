# Creates SQLite db, defines tables, imports cleaned CSVs to use
import sqlite3
import pandas as pd

# Connect to database file, create a cursor to execute SQL commands
conn = sqlite3.connect("world.db")  # creates file if it doesn't exist
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON") # needed to enable foreign keys

# Creating multiple tables with executescript
cursor.executescript("""
    DROP TABLE IF EXISTS indicators;
    DROP TABLE IF EXISTS economy;
    DROP TABLE IF EXISTS cities;
    DROP TABLE IF EXISTS countries;

    CREATE TABLE IF NOT EXISTS countries (
        iso_code TEXT PRIMARY KEY, 
        name TEXT NOT NULL, 
        region TEXT,
        area INTEGER
    );

    CREATE TABLE IF NOT EXISTS cities (
        name TEXT NOT NULL, 
        country TEXT, 
        iso2 TEXT NOT NULL,
        region TEXT,
        latitude REAL,
        longitude REAL,
        population INTEGER,
        elevation INTEGER,
        timezone TEXT,
        feature_code TEXT,
        FOREIGN KEY (iso2) REFERENCES countries(iso_code)
    );

    CREATE TABLE IF NOT EXISTS economy (
        iso_code TEXT NOT NULL, 
        name TEXT NOT NULL,
        gdp_ppp INTEGER,
        gdp_per_capita INTEGER,
        inflation REAL,
        unemployment REAL,
        public_debt_pct REAL,
        gdp INTEGER,
        FOREIGN KEY (iso_code) REFERENCES countries(iso_code)
    );

    CREATE TABLE IF NOT EXISTS indicators (
        iso_code TEXT NOT NULL, 
        name TEXT NOT NULL,
        population INTEGER,
        birth_rate REAL,
        death_rate REAL,
        life_expectancy REAL,
        literacy_rate REAL,
        density REAL,
        hdi REAL,
        FOREIGN KEY (iso_code) REFERENCES countries(iso_code)
    );
""")

# Loading CSVs into SQLite
countries = pd.read_csv("./data/clean/countries.csv")
countries.to_sql("countries", conn, if_exists="append", index=False)

cities = pd.read_csv("./data/clean/cities.csv")
cities.to_sql("cities", conn, if_exists="append", index=False)

economy = pd.read_csv("./data/clean/economy.csv")
economy.to_sql("economy", conn, if_exists="append", index=False)

indicators = pd.read_csv("./data/clean/indicators.csv")
indicators.to_sql("indicators", conn, if_exists="append", index=False)

# Commit changes and save to db file
conn.commit()
conn.close()