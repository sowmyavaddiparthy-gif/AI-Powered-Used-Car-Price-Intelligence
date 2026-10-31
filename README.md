# 🚗 AI-Powered Used-Car Price Intelligence and Fair-Price Recommendation System

An AI-powered web application that helps users make more informed used-car purchasing decisions through Machine Learning-based price prediction and AI-driven deal analysis.

## 📌 Project Overview

Buying a second-hand car can be challenging. Buyers often struggle to determine whether a seller's asking price is fair.

This project addresses that problem by combining a trained Machine Learning model with real-time web search and Generative AI.

Users enter a vehicle's specifications and asking price. The system predicts an estimated price, retrieves relevant online market information using Tavily, and uses Google Gemini to generate an analysis and buying recommendation.

## ✨ Key Features

* **Used-Car Price Prediction:** Estimates vehicle prices using a trained Random Forest Regression model.
* **Market Information Retrieval:** Retrieves relevant online used-car information through the Tavily Search API.
* **AI-Powered Deal Analysis:** Uses Google Gemini to analyse the predicted price, seller's asking price, and retrieved search results.
* **Buying Recommendation:** Generates an AI-assisted recommendation to help users evaluate a deal.
* **Price Comparison:** Compares the seller's asking price with the Machine Learning prediction.
* **Interactive Dashboard:** Provides an intuitive interface built with Streamlit.

## ⚙️ Technologies Used

| Technology              | Purpose                             |
| ----------------------- | ----------------------------------- |
| Python                  | Core programming language           |
| Pandas & NumPy          | Data processing and analysis        |
| Scikit-learn            | Machine Learning model development  |
| Random Forest Regressor | Used-car price prediction           |
| Streamlit               | Interactive web application         |
| Tavily Search API       | Online market information retrieval |
| Google Gemini API       | AI-powered deal analysis            |
| Jupyter Notebook        | Data exploration and analysis       |

## 🔄 System Workflow

1. **User Input:** Enter the car's name, specifications, and seller's asking price.
2. **Data Processing:** Prepare the input features for the trained model.
3. **Price Prediction:** Generate an estimated car price using the Random Forest model.
4. **Market Search:** Retrieve relevant online information using Tavily.
5. **AI Analysis:** Send the prediction, asking price, and search results to Google Gemini.
6. **Recommendation:** Display the price comparison, deal analysis, and buying recommendation through the Streamlit dashboard.

## 🏗️ Project Structure

```text
AI-Powered-Used-Car-Price-Intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── market_data/
│   ├── tavily_search_results.csv
│   └── used_car_listings.csv
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

## 🖥️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sowmyavaddiparthy-gif/AI-Powered-Used-Car-Price-Intelligence.git
cd AI-Powered-Used-Car-Price-Intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API keys

Create a `.env` file in the project root directory and add your own API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholders with your actual API keys.

**Important:** Never upload your `.env` file or expose your API keys publicly.

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your default web browser.

## 🤖 Machine Learning Model

The project uses a trained Random Forest Regression model to estimate used-car prices.

The model considers the following vehicle features:

* Manufacturing year
* Kilometres driven
* Fuel type
* Seller type
* Transmission
* Previous ownership
* Mileage
* Engine capacity
* Maximum power
* Number of seats

The trained model is stored in the `models/` directory.

## 🔮 Future Enhancements

* Improve the collection of individual used-car listings from reliable sources.
* Expand the training dataset with additional vehicle models and brands.
* Experiment with other Machine Learning algorithms.
* Introduce vehicle comparison functionality.
* Deploy the application online.

## ⚠️ Disclaimer

The predicted car price is an estimate based on historical training data and is not a guaranteed market value. Online search results provide additional market context and may not represent verified, currently available individual listings.

Users should independently verify vehicle details, condition, ownership documents, and service history before making a purchase.

## 👩‍💻 Project Information

**Project:** AI-Powered Used-Car Price Intelligence and Fair-Price Recommendation System

**Domain:** Machine Learning | Artificial Intelligence | Web Development

**Developed using:** Python, Streamlit, Scikit-learn, Tavily API, and Google Gemini API.

---

*Built to explore how Machine Learning and Generative AI can support smarter real-world purchasing decisions.*
