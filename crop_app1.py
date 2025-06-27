import streamlit as st
import pandas as pd
import joblib
import requests
from deep_translator import GoogleTranslator
import time
import os

# Load the trained model
model = joblib.load('crop_model.pkl')

# Profit estimation for each crop
profit_estimates = {
    'rice': 50000, 'maize': 40000, 'chickpea': 45000, 'kidneybeans': 47000,
    'pigeonpeas': 48000, 'mothbeans': 42000, 'mungbean': 43000, 'blackgram': 44000,
    'lentil': 46000, 'pomegranate': 70000, 'banana': 60000, 'mango': 65000,
    'grapes': 75000, 'watermelon': 55000, 'muskmelon': 50000, 'apple': 80000,
    'orange': 70000, 'papaya': 60000, 'coconut': 65000, 'cotton': 45000,
    'jute': 40000, 'coffee': 85000
}

# Local image mapping (Make sure file names match these)
crop_images = { 
    'rice': 'images/rice.jpeg',
    'maize': 'images/maize.jpeg',
    'chickpea': 'images/chickpea.jpeg',
    'kidneybeans': 'images/kidneybeans.jpeg',
    'pigeonpeas': 'images/pigeonpeas.jpeg',
    'mothbeans': 'images/mothbeans.jpeg',
    'mungbean': 'images/mungbean.jpeg',
    'blackgram': 'images/blackgram.jpeg',
    'lentil': 'images/lentil.jpeg',
    'pomegranate': 'images/pomegranate.jpeg',
    'banana': 'images/banana.jpeg',
    'mango': 'images/mango.jpeg',
    'grapes': 'images/grapes.jpeg',
    'watermelon': 'images/watermelon.jpeg',
    'muskmelon': 'images/muskmelon.jpeg',
    'apple': 'images/apple.jpeg',
    'orange': 'images/orange.jpeg',
    'papaya': 'images/papaya.jpeg',
    'coconut': 'images/coconut.jpeg',
    'cotton': 'images/cotton.jpeg',
    'jute': 'images/jute.jpeg',
    'coffee': 'images/coffee.jpeg'
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
    page_title="🌾 Smart Crop Recommendation",
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
    .stButton > button {
        background-color: #008080;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌾 Smart Crop Suggestion System")
st.caption("Multi-Language, Mobile-Friendly, Easy-to-Use Crop Recommendation App")

st.divider()

# Sidebar Inputs
st.sidebar.header("📋 Enter Soil and Rainfall Details")

N = st.sidebar.number_input("Nitrogen (N) (0 - 140)", min_value=0, max_value=500, value=90)
P = st.sidebar.number_input("Phosphorous (P) (5 - 145)", min_value=0, max_value=500, value=40)
K = st.sidebar.number_input("Potassium (K) (5 - 205)", min_value=0, max_value=500, value=45)
ph = st.sidebar.number_input("Soil pH (3.5 - 9.5)", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.sidebar.number_input("Rainfall (mm) (20 - 300)", min_value=0, max_value=500, value=200)

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

# Language codes for deep_translator
language_codes = {
    "English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta", "Kannada": "kn",
    "Marathi": "mr", "French": "fr", "German": "de", "Chinese": "zh-CN", "Japanese": "ja",
    "Spanish": "es", "Arabic": "ar", "Russian": "ru"
}

# Weather API Key
api_key = "1958487648d4249a43c5c14d45756acc"  # Replace with your OpenWeatherMap API key

# Main UI block
st.markdown('<div class="main">', unsafe_allow_html=True)

st.subheader("📊 Prediction Dashboard")

if st.button("🌱 Suggest the Best Crop"):
    with st.spinner('⏳ Fetching weather and predicting...'):
        time.sleep(2)
        temp, humidity = get_weather(city, api_key)

    if temp is not None:
        # Input validation
        if not (0 <= N <= 140 and 5 <= P <= 145 and 5 <= K <= 205 and 3.5 <= ph <= 9.5 and 20 <= rainfall <= 300):
            st.error("❌ No crop can grow in this soil condition.")
        else:
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

            # Translation
            target_language = language_codes.get(language, "en")
            if language != "English":
                translated_crop = GoogleTranslator(source='en', target=target_language).translate(prediction)
                st.success(f"✅ Recommended Crop (English): {prediction}")
                st.info(f"🌍 Recommended Crop ({language}): {translated_crop}")
            else:
                st.success(f"✅ Recommended Crop: {prediction}")

            st.write(f"🌡️ **Current Temperature:** {temp}°C")
            st.write(f"💧 **Current Humidity:** {humidity}%")

            # Estimated Profit
            profit = profit_estimates.get(prediction.lower(), 40000)
            st.write(f"💰 **Estimated Profit:** ₹{profit} per acre")

            # Local image display
            if prediction.lower() in crop_images:
                st.image(crop_images[prediction.lower()], caption=f"Suggested Crop: {prediction}", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/600x400.png?text=No+Image+Available", caption="No specific image found", use_container_width=True)

    else:
        st.error("❌ Could not fetch weather. Please check the city name or your internet connection.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("💡 Smart Solutions for Modern Agriculture | Multi-Language Support | Mobile Friendly")





