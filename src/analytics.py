import pandas as pd
from load import get_engine

def team_form(team_name: str, last_n: int = 5) -> pd.DataFrame:
    """Get a team's most recent results and rolling form."""
    engine = get_engine()
    query = f"""
    SELECT fm.date_id, ht.team_name AS home, at.team_name AS away,
           fm.home_score, fm.away_score
    FROM fact_match fm
    JOIN dim_team ht ON fm.home_team_id = ht.team_id
    JOIN dim_team at ON fm.away_team_id = at.team_id
    WHERE ht.team_name = '{team_name}' OR at.team_name = '{team_name}'
    ORDER BY fm.date_id DESC
    LIMIT {last_n}
    """
    return pd.read_sql(query, engine)

def goals_per_matchday(competition_id: int) -> pd.DataFrame:
    """Average goals scored per matchday — useful for spotting scoring trends."""
    engine = get_engine()
    query = f"""
    SELECT matchday, AVG(home_score + away_score) AS avg_goals
    FROM fact_match
    WHERE competition_id = {competition_id}
    GROUP BY matchday
    ORDER BY matchday
    """
    return pd.read_sql(query, engine)

if __name__ == "__main__":
    print(team_form("Arsenal FC"))
    print(goals_per_matchday(2021))  # 2021 = Premier League's competition ID