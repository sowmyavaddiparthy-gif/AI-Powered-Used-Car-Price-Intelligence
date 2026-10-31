
import os
from pathlib import Path

import joblib
import pandas as pd
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai

# Locate the project folder and load API keys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Load the existing trained ML model
MODEL_PATH = PROJECT_ROOT / "modules" / "used_car_price_model.pkl"
if not MODEL_PATH.exists():
    MODEL_PATH = PROJECT_ROOT / "models" / "used_car_price_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Trained model not found in the modules or models folder."
    )

model = joblib.load(MODEL_PATH)

# Initialize APIs
tavily_key = os.getenv("TAVILY_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not tavily_key or not gemini_key:
    raise ValueError(
        "Check that TAVILY_API_KEY and GEMINI_API_KEY "
        "are present in the project's .env file."
    )

tavily = TavilyClient(api_key=tavily_key)
gemini = genai.Client(api_key=gemini_key)

def get_car_details():
    print("\n=== USED-CAR PRICE INTELLIGENCE ===")
    print("Enter the car details below.\n")

    car = {
        "year": int(input("Manufacturing year: ")),
        "km_driven": float(input("Kilometres driven: ")),
        "fuel": input("Fuel type (Petrol/Diesel/CNG/LPG/Electric): ").strip(),
        "seller_type": input("Seller type (Individual/Dealer/Trustmark Dealer): ").strip(),
        "transmission": input("Transmission (Manual/Automatic): ").strip(),
        "owner": input("Owner (First Owner/Second Owner/Third Owner): ").strip(),
        "mileage(km/ltr/kg)": float(input("Mileage (km/l): ")),
        "engine": float(input("Engine capacity (CC): ")),
        "max_power": float(input("Maximum power (bhp): ")),
        "seats": int(input("Number of seats: ")),
    }

    car_name = input("Car name/model: ").strip()
    asking_price = float(input("Seller's asking price (INR): "))

    return car_name, car, asking_price

def predict_price(car):
    car_df = pd.DataFrame([car])
    prediction = model.predict(car_df)[0]
    return float(prediction)

def search_market(car_name, car):
    query = (
        f"used {car_name} for sale price in India "
        f"{car['year']} {car['fuel']} "
        f"{car['transmission']} used car"
    )

    response = tavily.search(
        query=query,
        search_depth="basic",
        topic="general",
        max_results=5,
        include_answer=False,
    )

    results = response.get("results", [])

    if not results:
        return "No search results were returned."

    formatted_results = []

    for index, result in enumerate(results, start=1):
        formatted_results.append(
            f"Result {index}\n"
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Information: {result.get('content', '')}\n"
        )

    return "\n".join(formatted_results)

def analyze_deal(car_name, car, asking_price, predicted_price, search_results):
    price_difference = asking_price - predicted_price

    prompt = f"""
You are a helpful used-car buying assistant for a student project.

Analyze the following car and give a practical buying recommendation.

CAR DETAILS:
Car: {car_name}
Manufacturing year: {car['year']}
Kilometres driven: {car['km_driven']}
Fuel: {car['fuel']}
Transmission: {car['transmission']}
Ownership: {car['owner']}
Mileage: {car['mileage(km/ltr/kg)']} km/l
Engine: {car['engine']} CC
Maximum power: {car['max_power']} bhp
Seats: {car['seats']}

SELLER'S ASKING PRICE: ₹{asking_price:,.0f}
ML MODEL'S PREDICTED PRICE: ₹{predicted_price:,.0f}
Asking price minus predicted price: ₹{price_difference:,.0f}

TAVILY WEB SEARCH RESULTS:
{search_results}

Write the recommendation using these headings:

1. BUYING VERDICT
Say whether the price looks attractive, reasonable, or expensive based
on the model prediction and available search information.

2. PRICE ANALYSIS
Compare the asking price with the ML prediction. Explain the difference
in simple language. Use web prices only when the search results actually
provide them.

3. ADVANTAGES
Give relevant advantages of this car based on the supplied details.

4. DRAWBACKS AND RISKS
Mention possible disadvantages, ownership considerations, and what the
buyer should inspect before purchasing.

5. MARKET COMPARISON
Summarize useful information from the search results. Include source
names and URLs when available. Do not invent listings or prices.

6. FINAL RECOMMENDATION
Give a clear, practical recommendation and suggest what the buyer could
do next, such as negotiating or inspecting the car.

Be helpful, direct, and easy to understand. Do not claim that a web page
contains a specific car listing or price unless that information appears
in the supplied results. If market information is limited, still provide
a useful preliminary recommendation based on the ML prediction and car
details. Do not make the whole answer a disclaimer.
"""

    response = gemini.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text or "Gemini did not return an analysis."

def main():
    car_name, car, asking_price = get_car_details()

    print("\nPredicting the car price...")
    predicted_price = predict_price(car)

    print(f"\nML predicted price: ₹{predicted_price:,.0f}")

    print("\nSearching the web with Tavily...")
    search_results = search_market(car_name, car)

    print("\nSending car details and search results to Gemini...")
    recommendation = analyze_deal(
        car_name,
        car,
        asking_price,
        predicted_price,
        search_results,
    )

    print("\n" + "=" * 60)
    print("YOUR USED-CAR BUYING RECOMMENDATION")
    print("=" * 60)
    print(recommendation)
    print("=" * 60)

if __name__ == "__main__":
    main()