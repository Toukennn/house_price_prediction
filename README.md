# 🏠 California House Price Predictor

A machine learning project that predicts **median house values in California** using demographic and geographic features.  
The project includes a **trained ML model**, an **interactive Streamlit web app**, and a **reproducible training workflow**.

---

## 📌 Project Overview
This project is based on the California Housing dataset and demonstrates an **end-to-end ML workflow**:
- Data preprocessing & feature engineering
- Model training and evaluation
- Model serialization
- Interactive deployment with Streamlit

The app allows users to input location and housing statistics and receive a real-time price prediction.

---

## 🧠 Model
- **Algorithm:** HistGradientBoostingRegressor
- **Target:** Median house value
- **Key engineered features:**
  - Rooms per household
  - Bedrooms per household
  - Population per household
- **Input validation:** Real-world California latitude/longitude bounds are enforced to prevent invalid predictions

---

## 📂 Project Structure
```text
house-price-predictor/
├─ app/
│  ├─ app.py                  # Streamlit application
│  └─ hgb_final.joblib        # Trained model
├─ notebooks/
│  └─ house_price_predict.ipynb
├─ data/
│  └─ housing.csv
├─ README.md
├─ requirements.txt
├─ .gitignore
└─ LICENSE
