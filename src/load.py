import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.engine import URL
load_dotenv()

def get_engine():
    url = URL.create(
        drivername="postgresql",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
    )
    return create_engine(url)

def load_dataframe(df: pd.DataFrame, table_name: str, engine, if_exists="append"):
    """
    Load a DataFrame into Postgres, avoiding duplicate primary keys
    by deleting existing rows with matching IDs first (a simple upsert pattern).
    """
    df.to_sql(table_name, engine, if_exists=if_exists, index=False, method="multi")
    print(f"✅ Loaded {len(df)} rows into {table_name}")

def load_all(transformed: dict, date_df: pd.DataFrame):
    engine = get_engine()

    # Order matters: dimensions before facts (foreign key constraints)
    load_dataframe(transformed["teams"].drop_duplicates("team_id"), "dim_team", engine, if_exists="append")
    load_dataframe(transformed["competitions"].drop_duplicates("competition_id"), "dim_competition", engine, if_exists="append")
    load_dataframe(date_df, "dim_date", engine, if_exists="append")
    load_dataframe(transformed["matches"], "fact_match", engine, if_exists="append")