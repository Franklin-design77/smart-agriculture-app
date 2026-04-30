import streamlit as st
import requests
from datetime import datetime
from model import predict_crop

# -------------------------------
# 🌦️ Get Real-Time Weather
# -------------------------------
def get_weather(city):
    api_key = "1a7a7e3db141030c276fd6bef1b7660c"   # 🔑 Put your API key here
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return None, None

    temp = data['main']['temp']
    humidity = data['main']['humidity']

    return temp, humidity

# -------------------------------
# 💰 Profit Data
# -------------------------------
crop_prices = {
    "rice": 20,
    "wheat": 18,
    "maize": 22,
    "cotton": 50,
    "sugarcane": 30,
    "coffee": 120,
    "banana": 25,
    "apple": 80,
    "grapes": 60,
    "mango": 70,
    "chickpea": 45,
    "lentil": 55
}

# -------------------------------
# 🌱 Streamlit UI
# -------------------------------
st.title("🌱 AI Smart Agriculture App (Real-Time)")

# 📅 Show current date
today = datetime.now()
st.write("📅 Date:", today.strftime("%Y-%m-%d"))

# 🌍 City input
city = st.text_input("Enter City", "Chennai")

# Soil inputs
N = st.number_input("Nitrogen (N)", value=90)
P = st.number_input("Phosphorus (P)", value=40)
K = st.number_input("Potassium (K)", value=40)
ph = st.number_input("pH value", value=6.5)

# Rainfall (manual or default)
rainfall = st.number_input("Rainfall (mm)", value=200.0)

# -------------------------------
# 🌦️ Get Live Weather
# -------------------------------
if st.button("Get Real-Time Weather"):
    temp, humidity = get_weather(city)

    if temp is not None:
        st.success(f"🌡️ Temperature: {temp} °C")
        st.success(f"💧 Humidity: {humidity} %")
    else:
        st.error("❌ Could not fetch weather data")

# -------------------------------
# 🤖 Prediction
# -------------------------------
if st.button("Predict Crop"):
    temp, humidity = get_weather(city)

    if temp is None:
        st.error("❌ Weather data not available")
    else:
        crop = predict_crop(N, P, K, temp, humidity, ph, rainfall)
        profit = crop_prices.get(crop, "Not available")

        st.success(f"🌾 Recommended Crop: {crop}")
        st.info(f"💰 Estimated Profit: ₹{profit}/kg")