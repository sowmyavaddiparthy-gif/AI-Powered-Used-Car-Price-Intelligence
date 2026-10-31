
import sys
import re
from pathlib import Path

import streamlit as st

# =========================================================
# AUTOWISE — USED-CAR PRICE INTELLIGENCE
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from analyzer_car_deal import predict_price, search_market, analyze_deal

st.set_page_config(
    page_title="AutoWise | Car Deal Intelligence",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F3F6FA;
        color: #152238;
    }

    [data-testid="stHeader"] {
        background: rgba(243, 246, 250, 0.94);
    }

    [data-testid="stSidebar"] {
        background: #101B2D;
    }

    [data-testid="stSidebar"] * {
        color: #E8EFF8;
    }

    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    .hero {
        background: linear-gradient(125deg, #101B2D 0%, #173D54 65%, #0D766E 100%);
        border-radius: 22px;
        padding: 34px 36px;
        color: white;
        margin: 8px 0 26px 0;
        box-shadow: 0 12px 30px rgba(16, 27, 45, 0.12);
    }

    .hero-tag {
        color: #70E0D2;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        font-weight: 800;
        line-height: 1.2;
        margin: 0 0 12px 0;
    }

    .hero p {
        color: #D5E4F0;
        font-size: 15px;
        line-height: 1.7;
        margin: 0;
        max-width: 750px;
    }

    .section-heading {
        font-size: 23px;
        font-weight: 800;
        color: #152238;
        margin: 22px 0 5px 0;
    }

    .section-subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: white;
        border: 1px solid #E1E8F0;
        border-radius: 17px;
        padding: 21px;
        min-height: 135px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.035);
    }

    .metric-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 13px;
    }

    .metric-value {
        color: #14243B;
        font-size: 27px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: #64748B;
        font-size: 12px;
        margin-top: 8px;
    }

    .decision-card {
        border-radius: 20px;
        padding: 26px 28px;
        margin: 18px 0 22px 0;
        border: 1px solid #D7E5E8;
        background: white;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }

    .decision-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .decision-title {
        font-size: 30px;
        line-height: 1.25;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .decision-description {
        color: #475569;
        font-size: 14px;
        line-height: 1.7;
    }

    .mini-label {
        color: #64748B;
        font-size: 12px;
        font-weight: 700;
    }

    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #E1E8F0;
        border-radius: 18px;
        padding: 24px;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button {
        background: #0D9488;
        color: white;
        border: 0;
        border-radius: 11px;
        font-weight: 800;
        min-height: 48px;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button:hover {
        background: #0F766E;
        color: white;
    }

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #E1E8F0;
        border-radius: 13px;
    }

    .footer {
        color: #64748B;
        font-size: 12px;
        text-align: center;
        padding: 30px 0 15px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):
    return f"₹{value:,.0f}"

def get_decision(report):
    """
    Interpret the recommendation Gemini returned.
    If the wording is unclear, ask the user to inspect first
    instead of inventing a confident buying verdict.
    """
    text = str(report).lower()

    avoid_phrases = [
        "do not buy",
        "don't buy",
        "do not recommend",
        "not recommended",
        "not worth buying",
        "walk away",
        "avoid this car",
        "avoid buying",
        "not a good deal",
        "not advisable",
        "high risk",
    ]

    positive_phrases = [
        "go for it",
        "go ahead",
        "strong opportunity",
        "highly attractive",
        "attractive and favorable",
        "attractive and favourable",
        "good deal",
        "worth buying",
        "recommended to buy",
        "recommend buying",
    ]

    caution_phrases = [
        "only after inspection",
        "subject to inspection",
        "provided that inspection",
        "needs further inspection",
        "significant concerns",
        "major concerns",
        "serious concerns",
    ]

    if any(phrase in text for phrase in avoid_phrases):
        return (
            "DON'T GO FOR IT",
            "red",
            "The AI recommendation indicates that this purchase should be avoided.",
        )

    if any(phrase in text for phrase in caution_phrases):
        return (
            "INSPECT BEFORE DECIDING",
            "amber",
            "The recommendation indicates that further checks are needed before committing.",
        )

    if any(phrase in text for phrase in positive_phrases):
        return (
            "GO FOR IT — AFTER CHECKS",
            "green",
            "The AI recommendation is positive. Confirm the car's condition and documents before purchasing.",
        )

    return (
        "INSPECT BEFORE DECIDING",
        "amber",
        "The report does not contain a clear buying verdict. Review the full analysis before deciding.",
    )

def split_report(report):
    """
    Split a Markdown AI report into sections when the expected
    numbered headings are present. Keep the full report available
    even if Gemini uses a different format.
    """
    headings = [
        "BUYING VERDICT",
        "PRICE ANALYSIS",
        "ADVANTAGES",
        "DRAWBACKS AND RISKS",
        "MARKET COMPARISON",
        "FINAL RECOMMENDATION",
        "NEXT STEPS",
    ]

    text = str(report)
    sections = {}
    matches = list(
        re.finditer(
            r"(?im)^\s{0,3}#{0,4}\s*(?:\*\*)?\s*"
            r"(?:\d+\.\s*)?("
            + "|".join(re.escape(h) for h in headings)
            + r")\s*:?\s*(?:\*\*)?\s*$",
            text,
        )
    )

    for i, match in enumerate(matches):
        title = match.group(1).upper()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        content = re.sub(r"^\s*[:\-]+\s*", "", content)
        sections[title] = content

    return sections

def show_section(title, content, icon):
    if content and content.strip():
        st.markdown(f"### {icon} {title.title()}")
        st.markdown(content)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("# 🚘 AutoWise")
    st.caption("USED-CAR DEAL INTELLIGENCE")
    st.divider()

    st.markdown("### Your buying journey")
    st.markdown("①  Vehicle details")
    st.markdown("②  ML price prediction")
    st.markdown("③  Online market search")
    st.markdown("④  Gemini deal analysis")
    st.markdown("⑤  Final buying decision")

    st.divider()
    st.markdown("### Technology stack")
    st.markdown("🤖 Machine Learning")
    st.markdown("🔎 Tavily Search")
    st.markdown("✨ Google Gemini")
    st.markdown("🌐 Streamlit")

    st.divider()
    st.caption("Academic CSE project")

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">SMARTER DECISIONS. BETTER DEALS.</div>
        <h1>Know the price.<br>Choose with confidence.</h1>
        <p>
            An intelligent used-car buying assistant that combines
            machine-learning price estimates, web search and AI analysis
            to help you decide whether a car is worth considering.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# INPUT FORM
# =========================================================

st.markdown(
    '<div class="section-heading">01 &nbsp; Vehicle details</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">Tell us about the car and its asking price.</div>',
    unsafe_allow_html=True,
)

with st.form("vehicle_form"):
    st.markdown("#### 🚘 Basic information")

    c1, c2, c3 = st.columns(3)

    with c1:
        car_name = st.text_input(
            "Car model",
            value="Maruti Suzuki Swift VXI",
        )
        year = st.number_input(
            "Manufacturing year",
            min_value=1990,
            max_value=2026,
            value=2021,
            step=1,
        )
        km_driven = st.number_input(
            "Kilometres driven",
            min_value=0,
            max_value=1_000_000,
            value=45000,
            step=1000,
        )
        fuel = st.selectbox(
            "Fuel type",
            ["Petrol", "Diesel", "CNG", "LPG", "Electric"],
        )

    with c2:
        seller_type = st.selectbox(
            "Seller type",
            ["Individual", "Dealer", "Trustmark Dealer"],
        )
        transmission = st.selectbox(
            "Transmission",
            ["Manual", "Automatic"],
        )
        owner = st.selectbox(
            "Ownership",
            [
                "First Owner",
                "Second Owner",
                "Third Owner",
                "Fourth & Above Owner",
                "Test Drive Car",
            ],
        )
        mileage = st.number_input(
            "Mileage (km/l)",
            min_value=0.1,
            max_value=100.0,
            value=21.0,
            step=0.5,
        )

    with c3:
        engine = st.number_input(
            "Engine capacity (CC)",
            min_value=50,
            max_value=10000,
            value=1197,
            step=1,
        )
        max_power = st.number_input(
            "Maximum power (bhp)",
            min_value=1.0,
            max_value=2000.0,
            value=88.5,
            step=0.5,
        )
        seats = st.selectbox(
            "Number of seats",
            [2, 4, 5, 6, 7, 8, 9, 10],
            index=2,
        )
        asking_price = st.number_input(
            "Seller's asking price (₹)",
            min_value=1000,
            max_value=100_000_000,
            value=500000,
            step=10000,
        )

    st.markdown("---")
    submitted = st.form_submit_button(
        "✨  ANALYZE THIS DEAL",
        type="primary",
        use_container_width=True,
    )

# =========================================================
# RUN ANALYSIS
# =========================================================

if submitted:
    if not car_name.strip():
        st.error("Please enter a car model.")
    else:
        car = {
            "year": int(year),
            "km_driven": int(km_driven),
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "owner": owner,
            "mileage(km/ltr/kg)": float(mileage),
            "engine": float(engine),
            "max_power": float(max_power),
            "seats": int(seats),
        }

        try:
            progress = st.progress(0, text="Preparing your analysis...")

            progress.progress(15, text="Predicting the car price with ML...")
            predicted_price = predict_price(car)

            progress.progress(40, text="Searching online market information...")
            search_results = search_market(car_name.strip(), car)

            progress.progress(70, text="Gemini is evaluating this deal...")
            recommendation = analyze_deal(
                car_name.strip(),
                car,
                asking_price,
                predicted_price,
                search_results,
            )

            progress.progress(100, text="Analysis complete!")
            progress.empty()

            st.session_state["deal_result"] = {
                "car_name": car_name.strip(),
                "car": car,
                "asking_price": float(asking_price),
                "predicted_price": float(predicted_price),
                "recommendation": str(recommendation),
            }

        except Exception as error:
            st.error("The analysis could not be completed.")
            with st.expander("Technical error details"):
                st.exception(error)

# =========================================================
# RESULTS
# =========================================================

if "deal_result" in st.session_state:
    result = st.session_state["deal_result"]

    asking = result["asking_price"]
    predicted = result["predicted_price"]
    difference = asking - predicted
    report = result["recommendation"]

    verdict, verdict_color, verdict_description = get_decision(report)

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">02 &nbsp; Your deal dashboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="section-subtitle">Analysis for {result["car_name"]}</div>',
        unsafe_allow_html=True,
    )

    # Prominent final verdict
    palette = {
        "green": ("#E8F8F2", "#087F5B", "#B8E7D5"),
        "red": ("#FFF0F0", "#C0392B", "#F3C4C0"),
        "amber": ("#FFF7E6", "#9A6700", "#F0D9A6"),
    }

    bg, fg, border_color = palette[verdict_color]

    st.markdown(
        f"""
        <div class="decision-card"
             style="background:{bg}; border-color:{border_color};">
            <div class="decision-label">YOUR AI BUYING VERDICT</div>
            <div class="decision-title" style="color:{fg};">
                {verdict}
            </div>
            <div class="decision-description">
                {verdict_description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Price cards
    st.markdown("#### 💰 Price breakdown")
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SELLER'S ASKING PRICE</div>
                <div class="metric-value">{money(asking)}</div>
                <div class="metric-note">Price requested by the seller</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">ML ESTIMATED PRICE</div>
                <div class="metric-value">{money(predicted)}</div>
                <div class="metric-note">Prediction from your trained model</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">ASKING − ML ESTIMATE</div>
                <div class="metric-value">{money(difference)}</div>
                <div class="metric-note">Negative means asking price is lower</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Visual comparison
    st.markdown("#### 📈 Asking price vs ML estimate")

    st.caption(
        "This chart compares the seller's asking price with the model's estimate. "
        "It is not a guarantee of the car's actual market value."
    )

    chart_data = {
        "Price type": ["Seller's asking price", "ML estimated price"],
        "Price (₹)": [asking, predicted],
    }

    st.bar_chart(
        chart_data,
        x="Price type",
        y="Price (₹)",
        color="#0D9488",
    )

    # AI report sections
    sections = split_report(report)

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">03 &nbsp; AI deal insights</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Understand what makes this deal attractive or risky.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            show_section(
                "Advantages",
                sections.get("ADVANTAGES", ""),
                "✅",
            )

        with st.container(border=True):
            show_section(
                "Market comparison",
                sections.get("MARKET COMPARISON", ""),
                "🔎",
            )

    with right:
        with st.container(border=True):
            show_section(
                "Drawbacks and risks",
                sections.get("DRAWBACKS AND RISKS", ""),
                "⚠️",
            )

        with st.container(border=True):
            show_section(
                "Final recommendation",
                sections.get("FINAL RECOMMENDATION", ""),
                "🎯",
            )

    # Inspection checklist
    with st.expander("🧰 Pre-purchase inspection checklist"):
        st.markdown(
            """
            Before paying, check:

            - [ ] Service history and maintenance records
            - [ ] Accident, flood, rust and repaint history
            - [ ] Odometer reading and ownership documents
            - [ ] Engine, brakes, tyres, AC and electrical systems
            - [ ] Registration, insurance and pending challans
            - [ ] Test drive and independent mechanic inspection
            """
        )

    # Full Gemini output always available
    with st.expander("📄 Read the complete AI analysis"):
        st.markdown(report)

    st.caption(
        "AutoWise is a decision-support project. Predictions and AI analysis "
        "can be imperfect; verify the car's condition and documents before buying."
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <b>AutoWise</b> · AI-Powered Used-Car Price Intelligence
        <br><br>
        Machine Learning &nbsp; • &nbsp; Tavily Search &nbsp; • &nbsp; Gemini AI
        <br>
        
    </div>
    """,
    unsafe_allow_html=True,
)