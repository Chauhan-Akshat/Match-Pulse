import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

def fetch_completed_matches(competition_code="PL", season=None):
    """Pull completed matches for a competition (default: Premier League)."""
    url = f"{BASE_URL}/competitions/{competition_code}/matches"
    params = {"status": "FINISHED"}
    if season:
        params["season"] = season

    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # raises an error if the request failed

    data = response.json()
    print(f"✅ Fetched {len(data['matches'])} matches")
    return data["matches"]

if __name__ == "__main__":
    matches = fetch_completed_matches(season=2024)  # 2024 = the 2024/25 season
    print(matches[0])