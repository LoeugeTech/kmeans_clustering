import streamlit as st
import requests
import joblib
from streamlit_extras.let_it_rain import rain

# Load Model
model = joblib.load("model/model.pkl")

# Streamlit app title and description
st.title("Customer Segmentation with K-Means Clustering")
st.write("Enter the values for customer's annual income and spending score to predict customer's segmentation")

# Input fields
annual_income = st.number_input("Annual Income (k$):", min_value=0, max_value=200, step=1, value=15)
spending_score = st.number_input("Spending Score (1-100):", min_value=1, max_value=100, step=1, value=50)

# Show the emoji rain when the page is loaded
rain(emoji="🎈", font_size=54, falling_speed=5, animation_length="infinite")


if st.button("Predict Customer's Segmentation"):
    # API URL
    api_url = "http://127.0.0.1:8000/predict"
    
    # input data
    input_data = {
        "annual_income": annual_income,
        "spending_score": spending_score
    }
    
    # Make API request
    response = requests.post(api_url, json=input_data)
    
    if response.status_code == 200:
        # Get the predicted cluster label
        cluster_label = response.json().get("cluster")
        st.success(f"The customer belongs to {cluster_label}")


    else:
        st.error("Error: Unable to fetch prediction")

# Load Image
st.image("src/Figure_2.png", caption="Customer Segmentation with K-Mean Clustering", use_container_width=True)


