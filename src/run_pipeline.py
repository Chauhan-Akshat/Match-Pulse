from extract import fetch_completed_matches
from transform import transform_matches, generate_date_dim
from load import load_all

def run():
    print("🔄 Extracting...")
    raw = fetch_completed_matches(season=2024)
    print("🔄 Transforming...")
    transformed = transform_matches(raw)
    date_df = generate_date_dim(transformed["matches"])

    print("🔄 Loading...")
    load_all(transformed, date_df)

    print("✅ Pipeline complete!")

if __name__ == "__main__":
    run()