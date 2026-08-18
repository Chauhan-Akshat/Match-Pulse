import pandas as pd

def transform_matches(raw_matches: list) -> dict:
    """
    Transform raw API match data into clean DataFrames matching our star schema.
    Returns a dict of DataFrames: teams, competitions, matches
    """
    teams = {}
    competitions = {}
    match_rows = []

    for m in raw_matches:
        home = m["homeTeam"]
        away = m["awayTeam"]
        comp = m["competition"]

        # Collect unique teams (dict keyed by id avoids duplicates)
        teams[home["id"]] = {
            "team_id": home["id"],
            "team_name": home["name"],
            "short_name": home.get("shortName"),
            "tla": home.get("tla"),
            "crest_url": home.get("crest")
        }
        teams[away["id"]] = {
            "team_id": away["id"],
            "team_name": away["name"],
            "short_name": away.get("shortName"),
            "tla": away.get("tla"),
            "crest_url": away.get("crest")
        }

        competitions[comp["id"]] = {
            "competition_id": comp["id"],
            "competition_name": comp["name"],
            "country": m.get("area", {}).get("name")
        }

        match_rows.append({
            "match_id": m["id"],
            "competition_id": comp["id"],
            "date_id": m["utcDate"][:10],  # extract just the date part
            "home_team_id": home["id"],
            "away_team_id": away["id"],
            "home_score": m["score"]["fullTime"]["home"],
            "away_score": m["score"]["fullTime"]["away"],
            "status": m["status"],
            "matchday": m.get("matchday"),
            "season": str(m["season"]["startDate"][:4]) if "season" in m else None
        })

    return {
        "teams": pd.DataFrame(teams.values()),
        "competitions": pd.DataFrame(competitions.values()),
        "matches": pd.DataFrame(match_rows)
    }

def generate_date_dim(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Build the date dimension from the dates actually present in our matches."""
    dates = pd.to_datetime(matches_df["date_id"]).unique()
    date_df = pd.DataFrame({"date_id": dates})
    date_df["year"] = date_df["date_id"].dt.year
    date_df["month"] = date_df["date_id"].dt.month
    date_df["day"] = date_df["date_id"].dt.day
    date_df["day_of_week"] = date_df["date_id"].dt.day_name()
    date_df["is_weekend"] = date_df["date_id"].dt.dayofweek >= 5
    return date_df