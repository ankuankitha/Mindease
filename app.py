# app.py
"""
MindEase 2.0 — AI Emotional Wellness & Women's Health Companion
---------------------------------------------------------------
Features:
- Facial Emotion Detection (DeepFace + OpenCV)
- Text Emotion Analysis (Hugging Face)
- Spotify Mood Music
- Empathetic AI Chat
- Women’s Health Companion
- Voice Feedback (TTS)
"""

import os
import cv2
import random
import tempfile
import streamlit as st
from datetime import datetime
from deepface import DeepFace
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="🌷 MindEase 2.0", page_icon="🌸", layout="wide")

# ---------- Spotify Setup ----------
SPOTIFY_CREDS = {
    "client_id": "ceb612b54e414622b7bbf9e1454f6841",
    "client_secret": "92416ba62edb46879b47dcc2ff2f5387"
}

try:
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CREDS["client_id"],
        client_secret=SPOTIFY_CREDS["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    st.sidebar.success("🎵 Spotify connected successfully!")
except Exception as e:
    st.sidebar.warning(f"⚠️ Spotify connection failed: {e}")
    sp = None

# ---------- Load Models ----------
@st.cache_resource
def load_models():
    try:
        emo_model = pipeline("text-classification",
                             model="j-hartmann/emotion-english-distilroberta-base",
                             top_k=None)
    except Exception as e:
        st.error(f"Error loading emotion model: {e}")
        emo_model = None
    return emo_model

emo_model = load_models()

# ---------- Helper Functions ----------
def analyze_face_opencv(image):
    """Detect emotion using DeepFace + OpenCV"""
    if image is None:
        return "neutral"
    try:
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image

        # Save temp image for DeepFace
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
            cv2.imwrite(temp.name, image_rgb)
            result = DeepFace.analyze(img_path=temp.name, actions=["emotion"], enforce_detection=False)
            os.remove(temp.name)
        if isinstance(result, list):
            result = result[0]
        return result.get("dominant_emotion", "neutral")
    except Exception:
        return "neutral"

def analyze_text_emotion(text):
    if not text or emo_model is None:
        return "neutral"
    try:
        preds = emo_model(text)[0]
        return max(preds, key=lambda x: x["score"])["label"].lower()
    except Exception:
        return "neutral"

def get_spotify_playlist(mood):
    if sp is None:
        return None
    mood_map = {
        "sad": "healing",
        "angry": "calm",
        "fear": "peaceful",
        "happy": "happy",
        "joy": "happy",
        "neutral": "focus"
    }
    query = mood_map.get(mood, "relax")
    try:
        results = sp.search(q=f"{query} mood playlist", type="playlist", limit=5)
        playlists = results["playlists"]["items"]
        if playlists:
            choice = random.choice(playlists)
            return choice["external_urls"]["spotify"]
    except Exception:
        pass
    return None

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        filename = os.path.join(tempfile.gettempdir(), "voice.mp3")
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename
    except Exception:
        return None

# ---------- Women’s Companion ----------
def women_health_tips(flow, cramps, craving):
    tips = []
    if flow.lower() in ["bright red", "normal red"]:
        tips.append("🌹 Healthy flow! Stay hydrated and eat iron-rich foods.")
    elif flow.lower() in ["brown", "dark"]:
        tips.append("🫖 Old blood flow — try warm drinks and gentle walks.")
    elif flow.lower() in ["pink", "pale"]:
        tips.append("💪 Possible low iron — add spinach, lentils, beetroot.")
    if cramps.lower() == "severe":
        tips.append("🔥 Severe cramps? Use heat pad and magnesium-rich foods.")
    if craving.lower() == "chocolate":
        tips.append("🍫 Dark chocolate or dates are good alternatives!")
    if craving.lower() == "salty":
        tips.append("🥥 Replenish electrolytes with coconut water.")
    playlist = get_spotify_playlist("calm") or "https://open.spotify.com"
    return "\n".join(tips) + f"\n\n🎧 Relax with: {playlist}"

# ---------- Main App ----------
st.markdown("<h1 style='text-align:center; color:#8B5CF6;'>🌸 MindEase 2.0 🌸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your AI Therapist & Wellness Companion</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 General Companion", "🌼 Women’s Companion"])

# ---------- General Companion ----------
with tab1:
    st.subheader("💖 Tell me how you feel")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_img = st.camera_input("📸 Capture your face") or st.file_uploader("Or upload a photo", type=["jpg", "png"])
        user_text = st.text_area("💬 What's on your mind?", placeholder="I'm feeling a bit anxious today...")

    if st.button("✨ Analyze My Mood"):
        if uploaded_img is not None:
            file_bytes = uploaded_img.read()
            npimg = cv2.imdecode(
                np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR
            )
            face_emo = analyze_face_opencv(npimg)
        else:
            face_emo = "neutral"

        text_emo = analyze_text_emotion(user_text)
        mood = text_emo if text_emo != "neutral" else face_emo

        st.success(f"🧠 Detected Emotion: **{mood}**")
        playlist = get_spotify_playlist(mood)
        if playlist:
            st.markdown(f"[🎧 Listen to a {mood}-based Spotify playlist]({playlist})")

        response = f"I sense you might be feeling **{mood}**. Remember, emotions are valid — I'm here for you 💕"
        st.info(response)

        # TTS voice output
        voice_file = text_to_speech(response)
        if voice_file and os.path.exists(voice_file):
            st.audio(voice_file)

# ---------- Women’s Companion ----------
with tab2:
    st.subheader("🌼 Women’s Health & Wellness Tips")
    flow = st.selectbox("🩸 Flow color", ["Bright Red", "Dark", "Brown", "Pink"])
    cramps = st.selectbox("💢 Cramps level", ["Mild", "Moderate", "Severe"])
    craving = st.selectbox("🍰 Cravings", ["Chocolate", "Salty", "Fried", "None"])

    if st.button("💗 Get My Personalized Tips"):
        tips = women_health_tips(flow, cramps, craving)
        st.write(tips)
