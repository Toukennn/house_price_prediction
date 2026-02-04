import streamlit as st
import pandas as pd
import numpy as np
import joblib

LAT_MIN, LAT_MAX = 32.5, 42.1
LON_MIN, LON_MAX = -124.5, -114.1

# Important: this name MUST match what you used in training
def add_extra_features(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    # avoid division by zero safely
    households = X["households"].replace(0, np.nan)
    total_rooms = X["total_rooms"].replace(0, np.nan)

    X["rooms_per_household"] = X["total_rooms"] / households
    X["population_per_household"] = X["population"] / households
    X["bedrooms_per_room"] = X["total_bedrooms"] / total_rooms
    return X

st.set_page_config(page_title="House Price Predictor", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load("hgb_final.joblib")


model = load_model()

st.title("🏠 California House Price Prediction")
st.write(
    "This app predicts **median house value** using a tuned "
    "**HistGradientBoostingRegressor** pipeline."
)

st.divider()

# -------------------------
# Input form
# -------------------------
with st.form("input_form"):
    st.subheader("Enter house / area features")

    col1, col2 = st.columns(2)

    with col1:
        longitude = st.number_input(
            "Longitude",
            min_value=LON_MIN,
            max_value=LON_MAX,
            value=-119.4179, # CA-ish default
            step=0.0001,
            format="%.4f"
        )
        latitude = st.number_input(
            "Latitude",
            min_value=LAT_MIN,
            max_value=LAT_MAX,
            value=36.7783,   # CA-ish default
            step=0.0001,
            format="%.4f"
        )
        
        
        housing_median_age = st.number_input("Housing Median Age", min_value=0.0, value=41.0)
        median_income = st.number_input("Median Income", min_value=0.0, value=8.3252, format="%.4f")

    with col2:
        total_rooms = st.number_input("Total Rooms", min_value=0.0, value=880.0)
        total_bedrooms = st.number_input("Total Bedrooms", min_value=0.0, value=129.0)
        population = st.number_input("Population", min_value=0.0, value=322.0)
        households = st.number_input("Households", min_value=1.0, value=126.0)

    ocean_proximity = st.selectbox(
        "Ocean Proximity",
        options=["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
    )

    show_input = st.checkbox("Show input dataframe")
    submitted = st.form_submit_button("Predict")

# -------------------------
# Prediction
# -------------------------
if submitted:
    # Basic sanity checks (optional but helpful)
    if total_bedrooms > total_rooms and total_rooms > 0:
        st.warning("Total Bedrooms is greater than Total Rooms. Please double-check your inputs.")

    input_df = pd.DataFrame([{
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }])

    pred = model.predict(input_df)[0]

    st.success(f"Predicted Median House Value: **${pred:,.0f}**")

    if show_input:
        st.dataframe(input_df)

st.caption("Model: tuned HistGradientBoostingRegressor pipeline (loaded via joblib).")
