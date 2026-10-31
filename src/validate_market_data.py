
import pandas as pd
from pathlib import Path

# Locate the project folder
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "market_data" / "used_car_listings.csv"

# Load the market listings
df = pd.read_csv(file_path)

required_columns = [
    "listing_id", "car_name", "year", "km_driven",
    "fuel", "transmission", "owner", "asking_price",
    "location", "listing_date", "source_url"
]

print("========== MARKET DATA VALIDATION ==========")
print("Total listings:", len(df))

# 1. Check required columns
missing_columns = [
    col for col in required_columns if col not in df.columns
]
print("\nMissing columns:", missing_columns if missing_columns else "None")

if missing_columns:
    print("Cannot run remaining checks because columns are missing.")
    raise SystemExit

# 2. Check missing values
print("\nMissing values:")
print(df[required_columns].isnull().sum())

# 3. Check duplicate listing IDs
print("\nDuplicate listing IDs:", df["listing_id"].duplicated().sum())

# 4. Check invalid prices
df["asking_price"] = pd.to_numeric(df["asking_price"], errors="coerce")
invalid_prices = df["asking_price"].isna() | (df["asking_price"] <= 0)
print("Invalid asking prices:", invalid_prices.sum())

# 5. Check invalid years
df["year"] = pd.to_numeric(df["year"], errors="coerce")
invalid_years = df["year"].isna() | (df["year"] < 1900) | (df["year"] > 2026)
print("Invalid manufacturing years:", invalid_years.sum())

# 6. Check invalid kilometres driven
df["km_driven"] = pd.to_numeric(df["km_driven"], errors="coerce")
invalid_km = df["km_driven"].isna() | (df["km_driven"] < 0)
print("Invalid kilometre values:", invalid_km.sum())

# 7. Check source URLs
missing_urls = (
    df["source_url"].isna()
    | df["source_url"].astype(str).str.strip().eq("")
)
print("Missing source URLs:", missing_urls.sum())

# 8. Check collection dates
df["listing_date"] = pd.to_datetime(
    df["listing_date"], errors="coerce"
)
invalid_dates = df["listing_date"].isna()
print("Invalid collection dates:", invalid_dates.sum())

# 9. Check duplicate rows
print("Duplicate complete rows:", df.duplicated().sum())

print("\n========== VALIDATION COMPLETE ==========")

print("\n========== ROWS NEEDING REVIEW ==========")

# Check manufacturing years
print("\nInvalid year rows:")
print(df.loc[invalid_years, ["listing_id", "car_name", "year"]])

# Check kilometres driven
print("\nInvalid kilometre rows:")
print(df.loc[invalid_km, ["listing_id", "car_name", "km_driven"]])

# Check collection dates
print("\nInvalid date rows:")
print(df.loc[invalid_dates, ["listing_id", "car_name", "listing_date"]])
