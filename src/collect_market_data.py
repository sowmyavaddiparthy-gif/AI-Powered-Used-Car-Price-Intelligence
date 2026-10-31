
import os
import re
import csv
from datetime import date
from pathlib import Path
from tavily import TavilyClient
from dotenv import load_dotenv

# Find the project root and load the API key
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise ValueError("TAVILY_API_KEY not found in the project .env file.")

client = TavilyClient(api_key=api_key)

OUTPUT_FILE = PROJECT_ROOT / "market_data" / "tavily_search_results.csv"

FIELDS = [
    "listing_id",
    "car_name",
    "year",
    "km_driven",
    "fuel",
    "transmission",
    "owner",
    "asking_price",
    "location",
    "listing_date",
    "source_url",
    "source_title",
    "raw_snippet",
    "verification_status",
]

def extract_price(text):
    """Extract a clearly labelled rupee/lakh asking price when present."""
    patterns = [
        r"₹\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|crore|crores)?",
        r"Rs\.?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|lac|crore|crores)?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            amount = float(match.group(1).replace(",", ""))
            unit = (match.group(2) or "").lower()

            if unit in ("lakh", "lakhs", "lac"):
                amount *= 100000
            elif unit in ("crore", "crores"):
                amount *= 10000000

            return int(amount)

    return ""

def main():
    print("Collecting used-car search results for Visakhapatnam...")

    response = client.search(
        query=(
            "individual used car listings for sale in Visakhapatnam "
            "India car model asking price year kilometres driven"
        ),
        search_depth="basic",
        topic="general",
        max_results=5,
        include_domains=[
            "cardekho.com",
            "cars24.com",
            "carwale.com",
            "spinny.com",
        ],
        include_answer=False,
        include_raw_content=False,
        include_usage=True,
    )

    results = response.get("results", [])
    print("\n --- SEARCH RESULT TITLES---")
    for result in results:
        print("-",result.get("title","No title"))
    rows = []

    for result in results:
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        snippet = result.get("content", "").strip()
        text = f"{title}\n{snippet}"

                # Keep only likely individual used-car listing pages.
        url_lower = url.lower()
        title_lower = title.lower()

        used_car_sites = (
            "carwale.com",
            "cars24.com",
            "spinny.com",
            "cardekho.com",
            "olx.in",
        )

        is_car_site = any(site in url_lower for site in used_car_sites)

        is_individual_listing = any(
            word in url_lower
            for word in ["/used-car-details/", "/used-cars/", "/buy-used-car/"]
        )

        text_lower = text.lower()

        relevant = (
    any(word in text_lower for word in
        ["used car", "used cars", "second hand car",
         "second hand cars", "pre-owned car"])
    and any(word in text_lower for word in
            ["visakhapatnam", "vizag"])
)

        if not relevant:
            continue

        # A search result is not proof of an active individual listing.
        # Do not infer model year, mileage, fuel, owner, or transmission.
        rows.append({
            "listing_id": "",
            "car_name": title,
            "year": "",
            "km_driven": "",
            "fuel": "",
            "transmission": "",
            "owner": "",
            "asking_price": extract_price(text),
            "location": "Visakhapatnam",
            "listing_date": date.today().isoformat(),
            "source_url": url,
            "source_title": title,
            "raw_snippet": snippet,
            "verification_status": "unverified_search_result",
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write a separate output file; do not overwrite existing listings.
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSearch results received: {len(results)}")
    print(f"Relevant results saved: {len(rows)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("All saved results are marked unverified.")
    print("Tavily usage:", response.get("usage", "Not provided"))

if __name__ == "__main__":
    main()