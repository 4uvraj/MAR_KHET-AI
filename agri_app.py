import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from app.data_pipeline import get_dataframe
from app.ml_model import load_model
from app.predict import predict_price

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MAR-KHET AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
if "prediction" not in st.session_state:
    st.session_state.prediction = None

# ---------------- REMOVE STREAMLIT HEADER ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #070F1F; }

.title-text {
    font-size: 32px;
    font-weight: 700;
    color: white;
}

.subtitle-text { color: #94A3B8; }

.metric-card {
    background: linear-gradient(145deg,#0F172A,#020617);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #1E293B;
    text-align:center;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}

.stButton button {
    background: linear-gradient(90deg,#16A34A,#22C55E);
    color:white;
    border-radius:12px;
    height:46px;
    font-weight:600;
}

.info-box {
    background:#0F172A;
    padding:18px;
    border-radius:16px;
    border:1px solid #1E293B;
}

.ai-box {
    background: linear-gradient(145deg,#052e16,#022c22);
    padding:18px;
    border-radius:16px;
    border:1px solid #065F46;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return get_dataframe(limit=5000)

@st.cache_resource
def load_ml_model():
    return load_model()

df = load_data()
# ---------- FIX DATA TYPES ----------
df["Modal_Price"] = pd.to_numeric(df["Modal_Price"], errors="coerce")
df["Min_Price"] = pd.to_numeric(df["Min_Price"], errors="coerce")
df["Max_Price"] = pd.to_numeric(df["Max_Price"], errors="coerce")

df.dropna(subset=["Modal_Price"], inplace=True)

model, features = load_ml_model()

# ---------------- HEADER ----------------
col1, col2 = st.columns([6,2])

with col1:
    st.markdown("""
    <div class="title-text">🌾 MAR-KHET AI Intelligence</div>
    <div class="subtitle-text">AI Powered Market Intelligence Platform</div>
    """, unsafe_allow_html=True)

with col2:
    st.toggle("🌙 Dark Mode", value=True, disabled=True)

st.divider()

# ---------------- SIDEBAR ----------------
if st.session_state.sidebar_open:
    with st.sidebar:

        st.header("⚙ Market Inputs")

        crop = st.selectbox(
            "🌾 Crop",
            sorted(df["Commodity"].dropna().unique())
        )

        state = st.selectbox(
            "📍 State",
            sorted(df["State"].dropna().unique())
        )

        state_df = df[df["State"] == state]

        district = st.selectbox(
            "🏙 District",
            sorted(state_df["District"].dropna().unique())
        )

        month = st.slider("📅 Month",1,12,6)
        year = st.number_input("📆 Year",2005,2035,2026)

        predict_btn = st.button("🚀 Predict Price")


# ---------------- FILTER DATA ----------------
# ---------------- SMART FILTER DATA ----------------

filtered_df = df[
    (df["Commodity"] == crop) &
    (df["State"] == state) &
    (df["District"] == district)
]

# Fallback 1 → Remove District
if len(filtered_df) < 10:
    filtered_df = df[
        (df["Commodity"] == crop) &
        (df["State"] == state)
    ]

# Fallback 2 → Only Crop
if len(filtered_df) < 10:
    filtered_df = df[
        (df["Commodity"] == crop)
    ]


# ---------------- KPI DATA ----------------
# ---------------- KPI DATA ----------------
if len(filtered_df) > 3:

    latest_price = filtered_df["Modal_Price"].iloc[-1]
    avg_price = filtered_df["Modal_Price"].mean()

    if latest_price > avg_price:
        trend = "Upward"
        demand = "High"
        risk = "Medium"
    elif latest_price < avg_price:
        trend = "Downward"
        demand = "Low"
        risk = "High"
    else:
        trend = "Stable"
        demand = "Medium"
        risk = "Low"

else:
    latest_price = 0
    trend = "No Data"
    demand = "No Data"
    risk = "No Data"


# ---------------- PREDICTION BUTTON LOGIC ----------------
if predict_btn:
    try:
        st.session_state.prediction = predict_price(
            model=model,
            feature_columns=features,
            commodity=crop,
            state=state,
            year=year,
            month=month
        )
    except Exception as e:
        st.error(f"Prediction Error: {e}")

prediction = st.session_state.prediction

# ---------------- KPI CARDS ----------------
c1,c2,c3,c4 = st.columns(4)

display_price = prediction if prediction else latest_price

with c1:
    st.markdown(f'<div class="metric-card">💰 Price<br><h2>₹ {round(display_price)}</h2></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="metric-card">📈 Trend<br><h3>{trend}</h3></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="metric-card">🌾 Demand<br><h3>{demand}</h3></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="metric-card">⚠ Risk<br><h3>{risk}</h3></div>', unsafe_allow_html=True)

st.divider()

# ---------------- MAIN GRID ----------------
left, center, right = st.columns([1.3,2.5,1.8])

# ---------------- LEFT PANEL ----------------
with left:
    st.subheader("📊 Market Summary")

    st.markdown(f"""
    <div class="info-box">
    Crop: <b>{crop}</b><br>
    State: <b>{state}</b><br>
    District: <b>{district}</b><br>
    Month: <b>{month}</b><br>
    Year: <b>{year}</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CENTER GRAPH ----------------
# ---------------- CENTER GRAPH ----------------
with center:
    st.subheader("📈 Price Trend Analysis")

    if len(filtered_df) > 5:

        trend_df = filtered_df.sort_values("Arrival_Date").tail(60)

        fig, ax = plt.subplots()

        ax.plot(
            trend_df["Arrival_Date"],
            trend_df["Modal_Price"],
            marker="o"
        )

        ax.set_xlabel("Date")
        ax.set_ylabel("Price ₹")
        ax.set_title(f"{crop} Price Trend")

        st.pyplot(fig)

    else:
        st.info("Not enough data to show trend")


# ---------------- RIGHT PANEL ----------------
with right:
    st.subheader("🤖 AI Market Insight")

    if prediction:
        st.markdown(f"""
        <div class="ai-box">
        <b>Predicted Price:</b> ₹ {round(prediction)}<br><br>

        <b>Demand Trend:</b> {trend}<br>
        <b>Weather Risk:</b> {risk}<br><br>

        Demand for {crop} expected to stay strong in {state}.  
        Market conditions appear stable based on historical mandi data.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click Predict Price to generate AI insight")

    st.subheader("💬 MAR-KHET AI Chat")

    user_q = st.text_input("Ask Market Question")

    if user_q:
        st.success(f"AI Insight: Market likely stable for {crop} in {state}")
