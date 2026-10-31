# AI-Powered Used-Car Price Intelligence and Fair-Price Recommendation System

An AI-powered web application that helps users evaluate used-car deals by combining Machine Learning-based price prediction with AI-driven market analysis.

## Project Overview

Buying a second-hand car can be challenging because buyers may not know whether the seller's asking price is reasonable.

This project aims to make that decision easier by predicting a car's estimated market value and generating an AI-powered analysis of the deal.

Users enter the car's specifications and asking price. The application predicts an estimated price using a trained Machine Learning model, retrieves relevant web search results, and uses Google's Gemini AI to generate a buying recommendation.

## Key Features

* **Used-Car Price Prediction:** Predicts an estimated car price using a trained Random Forest model.
* **Market Information Retrieval:** Uses Tavily Search API to retrieve relevant used-car market information.
* **AI-Powered Deal Analysis:** Uses Google Gemini to analyse the predicted price, asking price and retrieved search results.
* **Buying Recommendation:** Provides a recommendation to help users evaluate a deal.
* **Price Comparison:** Displays the difference between the seller's asking price and the ML-predicted price.
* **Interactive Dashboard:** Provides a user-friendly interface built with Streamlit.

## Technologies Used

* Python
* Machine Learning
* Scikit-learn
* Pandas and NumPy
* Streamlit
* Google Gemini API
* Tavily Search API
* Jupyter Notebook

## System Workflow

1. User enters used-car details.
2. The trained Machine Learning model predicts the estimated car price.
3. Tavily Search retrieves relevant online market information.
4. Google Gemini analyses the prediction, asking price and search results.
5. The application displays the price comparison and AI-generated recommendation.

## Project Structure

```text
AI_Used_Car_Price_Intelligence/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── market_data/
│
├── models/
│   └── used_car_price_model.pkl
│
├── notebooks/
│   ├── 01_dataset_check.py
│   └── 02_exploratory_data_analysis.ipynb
│
└── src/
    ├── analyzer_car_deal.py
    ├── collect_market_data.py
    └── validate_market_data.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Used_Car_Price_Intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root directory and add:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholders with your own API keys.

**Never upload your `.env` file or share your API keys publicly.**

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Machine Learning Model

The project uses a trained Random Forest Regression model to estimate used-car prices based on vehicle specifications such as:

* Manufacturing year
* Kilometres driven
* Fuel type
* Seller type
* Transmission
* Ownership history
* Mileage
* Engine capacity
* Maximum power
* Number of seats

## Future Enhancements

* Improve market-data collection using reliable individual vehicle listings.
* Expand the dataset with more vehicle brands and models.
* Improve prediction accuracy with additional data and model experimentation.
* Add more advanced vehicle comparison features.
* Deploy the application online.

## Disclaimer

The predicted price is an estimate based on historical training data. Online search results provide additional market context and may not represent verified, currently available individual listings. Users should independently inspect a vehicle and verify its condition and documents before purchasing.

---

**Developed as a Machine Learning and AI-based academic project.**
