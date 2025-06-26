import streamlit as st
import pandas as pd
import joblib
import requests
from deep_translator import GoogleTranslator

# Load the trained model
model = joblib.load('crop_model.pkl')

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
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌾 Smart Crop Suggestion System")
st.caption("An Intelligent, Multi-Language, Farmer-Friendly Crop Recommendation App")

st.divider()

# Sidebar Inputs
st.sidebar.header("📋 Enter Soil and Rainfall Details")
N = st.sidebar.slider("Nitrogen (N)", 0, 200, 90)
P = st.sidebar.slider("Phosphorous (P)", 0, 200, 40)
K = st.sidebar.slider("Potassium (K)", 0, 200, 45)
ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 200)

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
api_key = "1958487648d4249a43c5c14d45756acc"  # Replace with your OpenWeatherMap API key

# Main content
st.markdown('<div class="main">', unsafe_allow_html=True)

st.subheader("📊 Prediction Dashboard")

if st.button("🌱 Suggest the Best Crop"):
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

    else:
        st.error("❌ Could not fetch weather. Please check the city name or your internet connection.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("💡 Smart Solutions for Modern Agriculture | Multi-Language Support | Mobile Friendly")


