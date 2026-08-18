# Match Pulse — Football Analytics Pipeline

A data engineering pipeline that extracts football match data, models it into a star schema warehouse, orchestrates daily loads with Airflow, and streams live match events via Kafka.

## Architecture
- **Batch ETL**: Python (requests, pandas) extracts completed matches from football-data.org, transforms into a star schema, loads into Postgres
- **Orchestration**: Airflow DAG runs the ETL daily, with automatic retries on failure
- **Warehouse**: Star schema (fact_match, fact_match_event, dim_team, dim_competition, dim_date) in Postgres
- **Streaming**: Kafka producer polls live matches and publishes score-change events; a consumer writes them into the warehouse in near-real-time
- **Analytics**: Team form and scoring trend queries over the warehouse

## Tech Stack
Python, Pandas, PostgreSQL, Apache Airflow, Apache Kafka, Docker Compose, SQLAlchemy

## Getting Started
1. Clone the repo
2. Copy `.env.example` to `.env` and add your football-data.org API key
3. `docker compose up -d`
4. Airflow UI: `http://localhost:8081` (admin/admin) — trigger the `match_pulse_etl` DAG
5. Run analytics: `python src/analytics.py`
6. (Optional) Start streaming: `python src/kafka_producer.py` and `python src/kafka_consumer.py` in separate terminals

## Known Limitations
- Load layer does simple appends, not upserts — re-running on identical data will hit primary key conflicts (a real upsert pattern with `ON CONFLICT` would fix this)
- Live event polling is interval-based (60s), not true push-based streaming, due to free-tier API constraints
- Analytics queries use string interpolation rather than parameterized queries — fine for personal use, would need hardening for production