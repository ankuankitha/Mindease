import streamlit as st
from fer import FER
import cv2
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3
import random
from transformers import pipeline

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="🌸 MindEase", page_icon="🧘", layout="wide")
st.title("🌸 MindEase — AI Therapist & Wellness Companion 🌸")

# -----------------------------
# SPOTIFY AUTH (Your Credentials)
# -----------------------------
SPOTIFY_CREDS = {
    "client_id": "ceb612b54e414622b7bbf9e1454f6841",
    "client_secret": "92416ba62edb46879b47dcc2ff2f5387",
}

try:
    sp_auth = SpotifyClientCredentials(
        client_id=SPOTIFY_CREDS["client_id"],
        client_secret=SPOTIFY_CREDS["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=sp_auth)
    st.sidebar.success("✅ Spotify Connected")
except Exception as e:
    sp = None
    st.sidebar.error("⚠️ Spotify not connected")

# -----------------------------
# MODELS
# -----------------------------
emo_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
face_detector = FER(mtcnn=True)

# -----------------------------
# FUNCTIONS
# -----------------------------
def analyze_face(img_array):
    """Detect emotion from face"""
    try:
        results = face_detector.detect_emotions(img_array)
        if results:
            dominant_emotion = max(results[0]["emotions"], key=results[0]["emotions"].get)
            return dominant_emotion
        else:
            return "neutral"
    except Exception:
        return "neutral"

def analyze_text(text):
    """Detect emotion from user input text"""
    try:
        preds = emo_model(text)[0]
        emotion = max(preds, key=lambda x: x["score"])["label"].lower()
        return emotion
    except Exception:
        return "neutral"

def spotify_playlist(mood):
    """Get Spotify playlist link based on mood"""
    if sp is None:
        return None
    mood_map = {
        "happy": "Happy Hits",
        "sad": "Healing Songs",
        "angry": "Calm Down",
        "fear": "Peaceful Piano",
        "neutral": "Focus Music",
        "surprise": "Good Vibes"
    }
    query = mood_map.get(mood, "Relaxing Songs")
    try:
        res = sp.search(q=query, type="playlist", limit=5)
        playlists = res["playlists"]["items"]
        if playlists:
            return random.choice(playlists)["external_urls"]["spotify"]
    except Exception:
        pass
    return None

def tts_output(text):
    """Convert bot response to speech"""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.save_to_file(text, "response.mp3")
        engine.runAndWait()
        return "response.mp3"
    except Exception:
        return None

# -----------------------------
# WOMEN'S HEALTH MODULE
# -----------------------------
def womens_tips(flow, cramps, craving):
    advice = []
    if flow in ["Bright Red", "Normal Red"]:
        advice.append("✅ Healthy flow! Stay hydrated and eat iron-rich foods.")
    elif flow in ["Brown", "Dark"]:
        advice.append("🫖 Old blood flow — try ginger tea and light exercise.")
    elif flow in ["Pink", "Pale"]:
        advice.append("💪 Possible low iron — include beetroot and lentils in diet.")
    if cramps == "Severe":
        advice.append("🔥 Try heat therapy and magnesium-rich foods.")
    if craving == "Chocolate":
        advice.append("🍫 Choose dark chocolate or dates instead.")
    playlist = spotify_playlist("calm") or "https://open.spotify.com"
    return "\n".join(advice) + f"\n🎧 Relax with: {playlist}"

# -----------------------------
# MAIN UI
# -----------------------------
tab1, tab2 = st.tabs(["💬 AI Therapist", "🌸 Women’s Companion"])

# === TAB 1: Emotion & Chat ===
with tab1:
    st.subheader("🧠 Emotion Detection & Empathetic Chat")

    img_file = st.camera_input("📸 Take a picture for emotion detection")
    user_text = st.text_area("💖 How are you feeling today?", placeholder="I'm feeling a bit anxious...")

    if st.button("✨ Analyze & Get Support"):
        if img_file:
            img = cv2.imdecode(np.frombuffer(img_file.read(), np.uint8), 1)
            face_emotion = analyze_face(img)
        else:
            face_emotion = "neutral"

        text_emotion = analyze_text(user_text) if user_text else "neutral"
        mood = text_emotion if text_emotion != "neutral" else face_emotion

        playlist = spotify_playlist(mood)
        response = f"Detected mood: **{mood.capitalize()}** 💬\n\nI'm here for you. Everything will be okay.\n\n🎧 Playlist: {playlist or 'Not found'}"
        st.markdown(response)

        audio_path = tts_output(response)
        if audio_path:
            st.audio(audio_path)

# === TAB 2: Women’s Health ===
with tab2:
    st.subheader("🌼 Personalized Wellness Advice")

    flow = st.selectbox("🩸 Flow color", ["Bright Red", "Dark", "Brown", "Pink"])
    cramps = st.selectbox("💢 Cramps level", ["Mild", "Moderate", "Severe"])
    craving = st.selectbox("🍰 Cravings", ["Chocolate", "Salty", "Fried", "None"])

    if st.button("💗 Get My Health Tips"):
        tips = womens_tips(flow, cramps, craving)
        st.success(tips)
