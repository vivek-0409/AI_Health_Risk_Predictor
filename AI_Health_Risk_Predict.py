import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# ---------------- Load API Key ----------------
load_dotenv("API.env")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found. Please check your API.env file.")
else:
    genai.configure(api_key=api_key)

# ---------------- Load Lottie Animations ----------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

robot_anim = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_u4yrau.json")
heart_anim = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")
celebrate_anim = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# ---------------- Risk Calculation ----------------
def calculate_risks(age, gender, systolic, diastolic, sugar, bmi, cholesterol, heart_rate):
    risks = {}
    if sugar > 126:
        risks["Diabetes"] = "High"
    elif sugar > 100:
        risks["Diabetes"] = "Moderate"
    else:
        risks["Diabetes"] = "Low"

    if systolic >= 140 or diastolic >= 90:
        risks["Hypertension"] = "High"
    elif systolic >= 120 or diastolic >= 80:
        risks["Hypertension"] = "Moderate"
    else:
        risks["Hypertension"] = "Low"

    if cholesterol > 240 or (systolic > 140 and age > 45):
        risks["Heart Disease"] = "High"
    elif cholesterol > 200:
        risks["Heart Disease"] = "Moderate"
    else:
        risks["Heart Disease"] = "Low"

    return risks

# ---------------- Gemini AI Advice ----------------
def get_gemini_advice(user_data, risk_results):
    try:
        # ✅ Correct model name
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are a futuristic AI medical assistant robot.
        User Health Data: {user_data}
        Calculated Risk Results: {risk_results}
        Task: Predict the user's health risks in friendly robot style.
        Add motivational tips and a disclaimer.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Error fetching AI advice: {e}"

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="AI Health Risk Predictor", page_icon="🤖", layout="wide")

# Stylish Neon Title
st.markdown("""
    <style>
    .neon-title {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff6ec4, #7873f5, #42d392, #ffcc70);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
        background-size: 300% 300%;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    <div style='text-align:center; margin-top:30px; margin-bottom:20px;'>
        <h1 class='neon-title'>🤖 AI Health Risk Predictor</h1>
    </div>
""", unsafe_allow_html=True)

# Greeting Section
st.markdown("""
<style>
.greeting-text {
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    color: #ffffff;
    padding: 15px;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    animation: bounce 2s infinite;
    text-shadow: 2px 2px 4px #000000, 4px 4px 8px #333333;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
</style>
<div class='greeting-text'>
    🤖 Hello! I am your AI health assistant robot. <br> Enter your details below 👇
</div>
""", unsafe_allow_html=True)

# ---------------- Inputs ----------------
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
systolic = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250)
diastolic = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150)
sugar = st.number_input("Fasting Blood Sugar (mg/dL)", min_value=50, max_value=300)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, format="%.1f")
cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400)
heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200)

# ---------------- Predict Button ----------------
if st.button("🔍 Predict Risk"):
    user_data = {
        "Age": age,
        "Gender": gender,
        "Systolic BP": systolic,
        "Diastolic BP": diastolic,
        "Sugar": sugar,
        "BMI": bmi,
        "Cholesterol": cholesterol,
        "Heart Rate": heart_rate
    }

    risk_results = calculate_risks(age, gender, systolic, diastolic, sugar, bmi, cholesterol, heart_rate)

    # Robot Advice Section
    st.subheader("🤖 Robot's Health Advice")
    advice = get_gemini_advice(user_data, risk_results)
    st.write(advice)

    # Animations
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st_lottie(robot_anim, height=200, key="robot")
    with col2:
        st.markdown("""
            <div style='text-align:center; padding: 20px;
                 background: linear-gradient(135deg, #1e9600, #fff200, #ff0000);
                 color: white; font-size: 32px; font-weight: bold;
                 border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.4);
                 text-shadow: 2px 2px 0px #000000, 4px 4px 0px #333333;
                 letter-spacing: 1px;'>
                🎉 YOU ARE SECURE 🎉
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st_lottie(heart_anim, height=200, key="heart")

    if all(r == "Low" for r in risk_results.values()):
        st_lottie(celebrate_anim, height=200, key="celebration_top")

    # Risk Cards
    st.subheader("📊 Risk Prediction")
    colors_map = {"Low": "green", "Moderate": "orange", "High": "red"}
    for disease, risk in risk_results.items():
        st.markdown(
            f"<div style='padding:10px; border-radius:10px; background-color:{colors_map[risk]}; color:white; font-weight:bold;'>{disease}: {risk}</div>",
            unsafe_allow_html=True
        )

    # ---------------- 3D Chart ----------------
    st.subheader("📊 Health Risk Chart")
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    diseases = list(risk_results.keys())
    levels = {"Low": 1, "Moderate": 2, "High": 3}
    xs = np.arange(len(diseases))
    ys = np.zeros(len(diseases))
    zs = np.zeros(len(diseases))
    dx = np.ones(len(diseases)) * 0.5
    dy = np.ones(len(diseases)) * 0.5
    dz = [levels[r] for r in risk_results.values()]

    norm = plt.Normalize(min(dz), max(dz))
    colors = cm.coolwarm(norm(dz))

    ax.bar3d(xs, ys, zs, dx, dy, dz, color=colors, shade=True)
    ax.set_facecolor("#f5f5f5")
    ax.grid(True)
    ax.set_xticks(xs)
    ax.set_xticklabels(diseases, rotation=20, ha='right')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Risk Level (1=Low, 2=Moderate, 3=High)')
    ax.set_title("Health Risk Levels", fontsize=16, fontweight="bold", color="purple")

    st.pyplot(fig)

