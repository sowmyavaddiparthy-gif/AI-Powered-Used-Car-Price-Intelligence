import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load API key
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError(
        "TAVILY_API_KEY not found. Check your .env file."
    )

client = TavilyClient(api_key=api_key)

try:
    print("Searching for used-car listings in Visakhapatnam...\n")

    # One search request; basic search to limit credit usage
    response = client.search(
        query=(
            "used cars for sale in Visakhapatnam India "
            "car model year kilometers driven asking price"
        ),
        search_depth="basic",
        topic="general",
        max_results=5,
        include_domains=[
            "cardekho.com",
            "cars24.com",
            "carwale.com",
            "spinny.com"
        ],
        include_answer=False,
        include_raw_content=False,
        include_usage=True
    )

    results = response.get("results", [])

    if not results:
        print("No relevant results found in the selected domains.")
    else:
        for i, result in enumerate(results, start=1):
            print(f"\n--- RESULT {i} ---")
            print("Title:", result.get("title", "Unavailable"))
            print("URL:", result.get("url", "Unavailable"))
            print("Details:", result.get("content", "Unavailable"))

    # Display usage information if returned by the API
    print("Response keys:",list(response.keys()))
    print("Number of results:",len(response.get("results",[])))
    usage = response.get("usage")
    if usage is not None:
        print("\nTavily usage information:", usage)

    print("\nSearch completed.")

except Exception as error:
    print("\nSearch failed.")
    print("Error type:", type(error).__name__)
    print("Details:", error)