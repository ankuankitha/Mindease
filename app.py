# app.py
"""
MindEase 2.0 — Your AI Friend Therapist & Women's Companion
------------------------------------------------------------
Features:
- Emotion detection (face + text)
- Empathetic AI chat
- Spotify mood playlists
- Women's health & self-care tips
- TTS voice responses
- Works with Streamlit Cloud
"""

import os, random, csv, cv2
from datetime import datetime
import numpy as np
from PIL import Image
import streamlit as st
from deepface import DeepFace
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3

# ---------- Spotify credentials ----------
SPOTIFY_CREDS = {
    "client_id": "ceb612b54e414622b7bbf9e1454f6841",
    "client_secret": "92416ba62edb46879b47dcc2ff2f5387"
}

try:
    sp_auth = SpotifyClientCredentials(
        client_id=SPOTIFY_CREDS["client_id"],
        client_secret=SPOTIFY_CREDS["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=sp_auth)
    print("✅ Spotify connected")
except Exception as e:
    print("⚠️ Spotify init failed:", e)
    sp = None


# ---------- Load models ----------
@st.cache_resource
def load_models():
    emo_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    chat_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    return emo_model, chat_model

emo_model, chat_model = load_models()


# ---------- Emotion Analysis ----------
def analyze_face(image: np.ndarray):
    """Use DeepFace to detect emotion from face image."""
    try:
        if image is None:
            return "neutral"
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(img_path=rgb, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        return result.get("dominant_emotion", "neutral")
    except Exception:
        return "neutral"

def analyze_text(text: str):
    """Use transformer model to detect emotion from text."""
    if not text.strip() or emo_model is None:
        return "neutral"
    try:
        preds = emo_model(text)[0]
        return max(preds, key=lambda x: x["score"])["label"].lower()
    except Exception:
        return "neutral"


# ---------- Spotify Mood Playlist ----------
def spotify_playlist(mood):
    if sp is None:
        return None
    mood_map = {
        "sad": "healing",
        "sadness": "healing",
        "angry": "calm",
        "anger": "calm",
        "fear": "peaceful",
        "joy": "happy",
        "happy": "happy",
        "neutral": "focus",
    }
    query = mood_map.get(mood, "relax")
    try:
        res = sp.search(q=f"{query} mood playlist", type="playlist", limit=5)
        playlists = res.get("playlists", {}).get("items", [])
        if playlists:
            pick = random.choice(playlists)
            return {
                "name": pick["name"],
                "url": pick["external_urls"]["spotify"],
                "image": pick["images"][0]["url"] if pick["images"] else None
            }
    except Exception:
        pass
    return None


# ---------- TTS ----------
def tts(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        filename = "voice.mp3"
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename if os.path.exists(filename) else None
    except Exception:
        return None


# ---------- Chatbot + Empathy ----------
def reply_with_empathy(user_text, mood, history):
    if chat_model is None:
        return f"I sense you might be feeling {mood}. I’m here with you 💕"
    context = "".join([f"User: {u}\nBot: {b}\n" for u, b in history[-3:]])
    prompt = f"{context}User: {user_text}\nBot:"
    output = chat_model(prompt, max_new_tokens=120, do_sample=True, temperature=0.7)[0]["generated_text"]
    return output.split("Bot:")[-1].strip()

def save_chat(user, bot, mood):
    with open("chat_history.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user, bot, mood])


# ---------- Women's Health Tips ----------
def women_health(flow_color, cramps, craving):
    advice = []
    if flow_color.lower() in ["bright red", "normal red"]:
        advice.append("🌹 Your flow looks healthy — keep hydrated and eat iron-rich foods.")
    elif flow_color.lower() in ["brown", "dark"]:
        advice.append("🫖 Old blood flow — try warm water, ginger tea, and light walks.")
    elif flow_color.lower() in ["pink", "pale"]:
        advice.append("💪 Possible low iron — eat spinach, lentils, and beetroot.")
    if cramps.lower() == "severe":
        advice.append("🔥 Severe cramps? Use heat pad, magnesium-rich foods, and deep breathing.")
    if craving.lower() == "chocolate":
        advice.append("🍫 Craving sweets? Choose dark chocolate or dates instead.")
    if craving.lower() == "salty":
        advice.append("🥥 Add electrolytes like coconut water.")
    playlist = spotify_playlist("calm")
    link = playlist["url"] if playlist else "https://open.spotify.com"
    return "\n".join(advice) + f"\n\n🎧 Relax with: {link}"


# ---------- Streamlit UI ----------
st.set_page_config(page_title="🌷 MindEase 2.0", layout="wide")

st.markdown("<h1 style='text-align:center; color:#8B5CF6;'>🌸 MindEase 2.0 🌸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Your AI Therapist & Wellness Companion</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 General Companion", "🌼 Women’s Companion"])

# ----------- General Companion -----------
with tab1:
    st.subheader("💖 Tell me how you feel today")

    # Webcam + Upload options
    st.markdown("📸 Capture your face or upload an image for emotion detection:")
    col1, col2 = st.columns(2)
    with col1:
        camera_img = st.camera_input("Capture from webcam")
    with col2:
        upload_img = st.file_uploader("Upload a selfie", type=["jpg", "jpeg", "png"])

    user_input = st.text_input("🗣️ Your thoughts:", placeholder="I'm feeling a bit stressed today...")

    if st.button("✨ Analyze & Chat"):
        if user_input:
            # Pick whichever image source was used
            image = None
            if camera_img:
                image = np.array(Image.open(camera_img))
            elif upload_img:
                image = np.array(Image.open(upload_img))

            # Analyze emotions
            face_emo = analyze_face(image)
            text_emo = analyze_text(user_input)
            mood = text_emo if text_emo != "neutral" else face_emo

            # Get Spotify + Empathetic reply
            playlist = spotify_playlist(mood)
            empathy = reply_with_empathy(user_input, mood, [])
            message = f"**Detected Emotion:** {mood}\n\n💬 {empathy}"
            st.success(message)

            # Spotify playlist card
            if playlist:
                st.markdown(f"### 🎵 Recommended Playlist: [{playlist['name']}]({playlist['url']})")
                if playlist['image']:
                    st.image(playlist['image'], width=300)

            # Voice output
            voice_path = tts(empathy)
            if voice_path:
                st.audio(voice_path)

            save_chat(user_input, empathy, mood)
        else:
            st.warning("Please type how you're feeling first 💬")


# ----------- Women’s Companion -----------
with tab2:
    st.subheader("🌙 Track your cycle & get personalized wellness tips")

    flow = st.selectbox("🩸 Blood color", ["Bright Red", "Dark", "Brown", "Pink"])
    cramps = st.selectbox("💢 Cramps level", ["Mild", "Moderate", "Severe"])
    craving = st.selectbox("🍰 Cravings", ["Chocolate", "Salty", "Fried", "None"])

    if st.button("💗 Get My Tips"):
        tips = women_health(flow, cramps, craving)
        st.info(tips)
