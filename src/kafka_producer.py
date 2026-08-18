import os
import time
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
TOPIC = "match-events"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def poll_live_matches():
    url = "https://api.football-data.org/v4/competitions/PL/matches"
    params = {"status": "LIVE"}
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["matches"]

def run_producer(poll_interval_seconds: int = 60):
    print(f"🔴 Producer started. Polling every {poll_interval_seconds}s...")
    seen_scores = {}  # track last known score per match to detect changes

    while True:
        try:
            matches = poll_live_matches()
            for m in matches:
                match_id = m["id"]
                current_score = (m["score"]["fullTime"]["home"], m["score"]["fullTime"]["away"])

                if seen_scores.get(match_id) != current_score:
                    event = {
                        "match_id": match_id,
                        "home_team": m["homeTeam"]["name"],
                        "away_team": m["awayTeam"]["name"],
                        "home_score": current_score[0],
                        "away_score": current_score[1],
                        "minute": m.get("minute"),
                        "event_type": "SCORE_UPDATE"
                    }
                    producer.send(TOPIC, event)
                    print(f"📤 Published: {event}")
                    seen_scores[match_id] = current_score

        except Exception as e:
            print(f"⚠️ Error polling: {e}")

        time.sleep(poll_interval_seconds)

if __name__ == "__main__":
    run_producer()