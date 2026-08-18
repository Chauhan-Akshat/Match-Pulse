import json
from kafka import KafkaConsumer
from sqlalchemy import text
from load import get_engine

consumer = KafkaConsumer(
    "match-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest"
)

def match_exists(engine, match_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM fact_match WHERE match_id = :match_id"),
            {"match_id": match_id}
        )
        return result.fetchone() is not None

def run_consumer():
    engine = get_engine()
    print("Consumer started, listening for events...")

    for message in consumer:
        event = message.value
        print(f"Received: {event}")

        if not match_exists(engine, event["match_id"]):
            print(f"Skipping event for match_id {event['match_id']} - not yet in fact_match (likely current season, not yet batch-loaded)")
            continue

        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO fact_match_event (match_id, event_type, minute, detail)
                    VALUES (:match_id, :event_type, :minute, :detail)
                """),
                {
                    "match_id": event["match_id"],
                    "event_type": event["event_type"],
                    "minute": event.get("minute"),
                    "detail": f"{event['home_team']} {event['home_score']} - {event['away_score']} {event['away_team']}"
                }
            )
            conn.commit()

if __name__ == "__main__":
    run_consumer()