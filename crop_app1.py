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

# Crop image URLs from your GitHub repo
crop_images = {
    'rice': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/rice.jpeg',
    'maize': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/maize.jpeg',
    'chickpea': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/chickpea.jpeg',
    'kidneybeans': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/kidneybeans.jpeg',
    'pigeonpeas': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/pigeonpeas.jpeg',
    'mothbeans': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/mothbeans.jpeg',
    'mungbean': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/mungbean.jpeg',
    'blackgram': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/blackgram.jpeg',
    'lentil': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/lentil.jpeg',
    'pomegranate': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/pomegranate.jpeg',
    'banana': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/banana.jpeg',
    'mango': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/mango.jpeg',
    'grapes': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/grapes.jpeg',
    'watermelon': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/watermelon.jpeg',
    'muskmelon': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/muskmelon.jpeg',
    'apple': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/apple.jpeg',
    'orange': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/orange.jpeg',
    'papaya': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/papaya.jpeg',
    'coconut': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/coconut.jpeg',
    'cotton': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/cotton.jpeg',
    'jute': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/jute.jpeg',
    'coffee': 'https://raw.githubusercontent.com/abhilashraavi/Crop-Suggestion-Project/main/images/coffee.jpg'
}

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
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #FF6347 !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌾 Smart Crop Suggestion System")
st.caption("An Intelligent, Multi-Language, Farmer-Friendly Crop Recommendation App")

st.divider()

# Sidebar Inputs
st.sidebar.header("📋 Enter Soil and Rainfall Details")
N = st.sidebar.number_input("Nitrogen (N) (Range: 0 - 200)", min_value=0, max_value=1000, value=90)
P = st.sidebar.number_input("Phosphorous (P) (Range: 0 - 200)", min_value=0, max_value=1000, value=40)
K = st.sidebar.number_input("Potassium (K) (Range: 0 - 200)", min_value=0, max_value=1000, value=45)
ph = st.sidebar.number_input("Soil pH (Range: 0.0 - 14.0)", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.sidebar.number_input("Rainfall (mm) (Range: 0 - 500)", min_value=0, max_value=1000, value=200)

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
api_key = "1958487648d4249a43c5c14d45756acc"

st.markdown('<div class="main">', unsafe_allow_html=True)
st.subheader("📊 Prediction Dashboard")

if st.button("🌱 Suggest the Best Crop"):
    # Validation Check
    if N > 200 or P > 200 or K > 200 or rainfall > 500:
        st.error("❌ No crop can grow in this soil and rainfall condition. Please enter valid ranges.")
    else:
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

            # Display Crop Image
            if prediction.lower() in crop_images:
                st.image(crop_images[prediction.lower()], caption=f"Suggested Crop: {prediction}", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/600x400.png?text=No+Image+Available", caption="No specific image found", use_container_width=True)

            # Example Profit Details (You can customize this based on real data)
            st.write("💰 **Expected Profit Details:**")
            st.info(f"For {prediction}, average profit per acre can range from ₹20,000 to ₹80,000 depending on market conditions, soil health, and farming practices.")

        else:
            st.error("❌ Could not fetch weather. Please check the city name or your internet connection.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")
st.caption("💡 Smart Solutions for Modern Agriculture | Multi-Language Support | Mobile Friendly")






