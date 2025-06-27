import streamlit as st
import pandas as pd
import joblib
import requests
from deep_translator import GoogleTranslator
import time

# Load the trained model
model = joblib.load('crop_model.pkl')

# Sample profit data (can be customized)
profit_estimates = {
    'rice': 30000,
    'maize': 25000,
    'chickpea': 35000,
    'kidneybeans': 40000,
    'pigeonpeas': 45000,
    'mothbeans': 28000,
    'mungbean': 32000,
    'blackgram': 37000,
    'lentil': 36000,
    'pomegranate': 80000,
    'banana': 100000,
    'mango': 90000,
    'grapes': 120000,
    'watermelon': 60000,
    'muskmelon': 55000,
    'apple': 150000,
    'orange': 75000,
    'papaya': 50000,
    'coconut': 70000,
    'cotton': 40000,
    'jute': 30000,
    'coffee': 100000
}

# Weather API function
def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp'], data['main']['humidity']
    else:
        return None, None

# Streamlit page configuration
st.set_page_config(
    page_title="🌾 Smart Crop Suggestion",
    page_icon="🌱",
    layout="centered"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 12px 26px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌾 Smart Crop Suggestion System")
st.caption("Multi-Language, Farmer-Friendly Crop Recommendation")

st.divider()

# Sidebar Inputs
st.sidebar.header("📋 Enter Soil and Rainfall Details")

# Manual input fields
N = st.sidebar.number_input("Nitrogen (N) [0 - 140]", min_value=0, max_value=1000, value=90)
P = st.sidebar.number_input("Phosphorous (P) [5 - 145]", min_value=0, max_value=1000, value=40)
K = st.sidebar.number_input("Potassium (K) [5 - 205]", min_value=0, max_value=1000, value=45)
ph = st.sidebar.number_input("Soil pH [3.5 - 9.5]", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.sidebar.number_input("Rainfall (mm) [20 - 300]", min_value=0, max_value=1000, value=200)

# City Input
st.sidebar.header("🌍 Location and Language")
city = st.sidebar.selectbox("Select Your City", ["Hyderabad,IN", "Mumbai,IN", "Chennai,IN", "Delhi,IN", "Other"])
if city == "Other":
    city = st.sidebar.text_input("Enter City Name (e.g., Pune,IN)")

# Language Selection
language = st.sidebar.selectbox(
    "Choose Output Language",
    ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Marathi", "French", "German", "Chinese", "Japanese", "Spanish", "Arabic", "Russian"]
)

# Language codes
language_codes = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Marathi": "mr",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Spanish": "es",
    "Arabic": "ar",
    "Russian": "ru"
}

# Weather API Key
api_key = "1958487648d4249a43c5c14d45756acc"  # Replace with your real API key

# Main Interface
st.markdown('<div class="main">', unsafe_allow_html=True)
st.subheader("📊 Prediction Dashboard")

if st.button("🌱 Suggest the Best Crop"):
    # Check input ranges
    if not (0 <= N <= 140 and 5 <= P <= 145 and 5 <= K <= 205 and 3.5 <= ph <= 9.5 and 20 <= rainfall <= 300):
        st.error("❌ No crop can grow in this soil condition. Please enter valid input ranges.")
    else:
        with st.spinner('⏳ Fetching weather and predicting...'):
            time.sleep(2)
            temp, humidity = get_weather(city, api_key)

        if temp is not None:
            input_data = pd.DataFrame([{
                'N': N,
                'P': P,
                'K': K,
                'temperature': temp,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }])

            prediction = model.predict(input_data)[0]

            target_language = language_codes.get(language, "en")

            if language != "English":
                translated_crop = GoogleTranslator(source='en', target=target_language).translate(prediction)
                st.success(f"✅ Recommended Crop (English): {prediction}")
                st.info(f"🌍 Recommended Crop ({language}): {translated_crop}")
            else:
                st.success(f"✅ Recommended Crop: {prediction}")

            st.write(f"🌡️ **Current Temperature:** {temp}°C")
            st.write(f"💧 **Current Humidity:** {humidity}%")

            # Show estimated profit
            profit = profit_estimates.get(prediction.lower(), 40000)
            st.write(f"💰 **Estimated Profit:** ₹{profit} per acre")

            # Display crop image if available
            image_url = f"https://source.unsplash.com/600x400/?{prediction},crop"
            st.image(image_url, caption=f"Suggested Crop: {prediction}", use_column_width=True)

        else:
            st.error("❌ Could not fetch weather. Please check the city name or your internet connection.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🌱 Smart Farming | Multi-Language Support | Mobile Friendly | Designed for Everyone")



