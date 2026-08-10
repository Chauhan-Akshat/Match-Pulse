-- Dimension: Teams
CREATE TABLE IF NOT EXISTS dim_team (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(50),
    tla VARCHAR(10),
    crest_url TEXT
);

-- Dimension: Competitions/Leagues
CREATE TABLE IF NOT EXISTS dim_competition (
    competition_id INTEGER PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

-- Dimension: Date 
CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week VARCHAR(10),
    is_weekend BOOLEAN
);

-- Fact: Match Results
CREATE TABLE IF NOT EXISTS fact_match (
    match_id INTEGER PRIMARY KEY,
    competition_id INTEGER REFERENCES dim_competition(competition_id),
    date_id DATE REFERENCES dim_date(date_id),
    home_team_id INTEGER REFERENCES dim_team(team_id),
    away_team_id INTEGER REFERENCES dim_team(team_id),
    home_score INTEGER,
    away_score INTEGER,
    status VARCHAR(20),
    matchday INTEGER,
    season VARCHAR(20)
);

-- Fact: Live Match Events 
CREATE TABLE IF NOT EXISTS fact_match_event (
    event_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES fact_match(match_id),
    event_type VARCHAR(30), -- GOAL, CARD, SUBSTITUTION, etc.
    minute INTEGER,
    team_id INTEGER REFERENCES dim_team(team_id),
    player_name VARCHAR(100),
    detail TEXT,
    ingested_at TIMESTAMP DEFAULT NOW()
);