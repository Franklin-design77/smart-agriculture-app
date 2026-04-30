import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from model import predict_crop, model

# -------------------------------
# 🌦️ Weather Function
# -------------------------------
def get_weather(city):
    try:
        api_key = "1a7a7e3db141030c276fd6bef1b7660c"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return 25, 70

        return data['main']['temp'], data['main']['humidity']
    except:
        return 25, 70


# -------------------------------
# 💰 Prices
# -------------------------------
crop_prices = {
    "rice": 20, "wheat": 18, "maize": 22, "cotton": 50,
    "sugarcane": 30, "coffee": 120, "banana": 25,
    "apple": 80, "grapes": 60, "mango": 70,
    "chickpea": 45, "lentil": 55
}

# -------------------------------
# 🎨 UI Config
# -------------------------------
st.set_page_config(page_title="Smart Agriculture AI", layout="wide")

st.title("🌱 Smart Agriculture AI (Advanced App)")

# Sidebar
st.sidebar.title("🌾 AI Farming Assistant")
menu = st.sidebar.radio("Menu", ["Home", "Map", "Chatbot"])

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
if menu == "Home":

    st.subheader("📅 Date")
    st.write(datetime.now().strftime("%Y-%m-%d"))

    # Location
    city = st.text_input("🌍 Enter City", "Chennai")

    # Soil
    col1, col2 = st.columns(2)
    with col1:
        N = st.number_input("Nitrogen", value=90)
        P = st.number_input("Phosphorus", value=40)
        K = st.number_input("Potassium", value=40)

    with col2:
        ph = st.number_input("pH", value=6.5)
        rainfall = st.number_input("Rainfall", value=200.0)

    # Weather
    temp, humidity = get_weather(city)

    st.info(f"🌡 Temp: {temp} °C | 💧 Humidity: {humidity}%")

    # Prediction
    if st.button("🚜 Predict Crop"):
        crop = predict_crop(N, P, K, temp, humidity, ph, rainfall)
        profit = crop_prices.get(crop.lower(), 50)

        st.success(f"🌾 Crop: {crop}")
        st.info(f"💰 Profit: ₹{profit}/kg")

        # 📊 Graph
        probs = model.predict_proba([[N, P, K, temp, humidity, ph, rainfall]])[0]
        crops = model.classes_

        df = pd.DataFrame({
            "Crop": crops,
            "Probability": probs
        }).sort_values(by="Probability", ascending=False).head(5)

        st.subheader("📊 Top Predictions")
        st.bar_chart(df.set_index("Crop"))

# -------------------------------
# 🗺️ MAP PAGE
# -------------------------------
elif menu == "Map":

    st.subheader("🗺️ Select Location")

    map_data = pd.DataFrame({
        "lat": [13.0827],
        "lon": [80.2707]
    })

    st.map(map_data)

    st.info("📍 Default location: Chennai")

# -------------------------------
# 🤖 CHATBOT PAGE
# -------------------------------
elif menu == "Chatbot":

    st.subheader("🤖 AI Farming Assistant")

    user_input = st.text_input("Ask something about farming:")

    if user_input:
        response = ""

        if "crop" in user_input.lower():
            response = "You can use the prediction tool to find the best crop."
        elif "soil" in user_input.lower():
            response = "Healthy soil should have balanced NPK values."
        elif "weather" in user_input.lower():
            response = "Weather plays a key role in crop selection."
        else:
            response = "I can help with crop suggestions, soil, and farming tips."

        st.success(response)
