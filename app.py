
import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("retail_sales_model.pkl")
features = joblib.load("retail_features.pkl")

st.set_page_config(
    page_title="Retail Sales Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Prediction & Inventory Dashboard")
st.write("AI-powered retail sales forecasting and inventory monitoring")

st.divider()

# Sidebar inputs
st.sidebar.header("Sales Prediction")

year = st.sidebar.number_input("Year", 2026, 2030, 2026)
month = st.sidebar.slider("Month", 1, 12, 8)
day = st.sidebar.slider("Day", 1, 31, 28)
day_of_week = st.sidebar.slider("Day of Week", 0, 6, 4)
week = st.sidebar.slider("Week", 1, 53, 35)

promo_flag = st.sidebar.selectbox(
    "Promotion",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

revenue = st.sidebar.number_input("Expected Revenue", min_value=0.0, value=5000.0)
lag_1 = st.sidebar.number_input("Previous Day Sales", min_value=0.0, value=5.0)
lag_7 = st.sidebar.number_input("7-Day Lag Sales", min_value=0.0, value=30.0)
lag_30 = st.sidebar.number_input("30-Day Lag Sales", min_value=0.0, value=25.0)
rolling_7 = st.sidebar.number_input("7-Day Average Sales", min_value=0.0, value=28.0)
rolling_30 = st.sidebar.number_input("30-Day Average Sales", min_value=0.0, value=27.0)

if st.sidebar.button("Predict Sales"):

    input_data = pd.DataFrame([[
        year, month, day, day_of_week, week,
        promo_flag, revenue, lag_1, lag_7, lag_30,
        rolling_7, rolling_30
    ]], columns=features)

    prediction = model.predict(input_data)[0]

    st.subheader("Predicted Sales")
    st.metric("Expected Units Sold", f"{max(0, prediction):.0f}")

    st.success("Sales prediction generated successfully!")

st.divider()

st.subheader("📦 Inventory Monitoring")

inventory_file = "inventory_analysis.csv"

try:
    inventory = pd.read_csv(inventory_file)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        len(inventory)
    )

    col2.metric(
        "Out of Stock",
        (inventory["on_hand_units"] == 0).sum()
    )

    col3.metric(
        "Reorder Required",
        (inventory["on_hand_units"] <= inventory["reorder_point"]).sum()
    )

except:
    st.warning("Inventory analysis file not found.")
