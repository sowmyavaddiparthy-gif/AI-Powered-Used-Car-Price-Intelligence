
import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "API key not found. Please check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=api_key)

try:
    # Test ordinary text generation without Google Search
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with: Gemini API connection successful."
    )

    print("\n--- GEMINI RESPONSE ---\n")
    print(response.text)

except Exception as error:
    print("\nGemini test failed.")
    print("Error type:", type(error).__name__)
    print("Details:", error)