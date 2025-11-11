"""
MindEase 2.0 — AI Therapist & Women's Wellness Companion
---------------------------------------------------------
Streamlit version with Spotify, Emotion AI, and Wellness Guidance
"""

import os
import random
import csv
from datetime import datetime
import streamlit as st
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3

# ---------------- SPOTIFY SETUP ----------------
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
    st.sidebar.success("✅ Spotify connected")
except Exception as e:
    st.sidebar.warning(f"⚠️ Spotify init failed: {e}")
    sp = None

# ---------------- EMOTION MODELS ----------------
@st.cache_resource
def load_models():
    try:
        emo_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    except Exception:
        emo_model = None
    try:
        chat_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    except Exception:
        chat_model = None
    return emo_model, chat_model

emo_model, chat_model = load_models()

# ---------------- HELPERS ----------------
def analyze_text(text):
    if not text.strip() or emo_model is None:
        return "neutral"
    try:
        preds = emo_model(text)[0]
        return max(preds, key=lambda x: x["score"])["label"].lower()
    except Exception:
        return "neutral"

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
            return pick["external_urls"]["spotify"]
    except Exception:
        pass
    return None

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

def reply_with_empathy(user_text, mood, history):
    if chat_model is None:
        return f"I sense you might be feeling {mood}. I’m here with you 💕"
    context = "".join([f"User: {u}\nBot: {b}\n" for u, b in history[-3:]])
    prompt = f"{context}User: {user_text}\nBot:"
    try:
        output = chat_model(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)[0]["generated_text"]
        return output.split("Bot:")[-1].strip()
    except Exception:
        return f"I understand you're feeling {mood}. I’m here to listen 💗"

def save_chat(user, bot, mood):
    with open("chat_history.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user, bot, mood])

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
    playlist = spotify_playlist("calm") or "https://open.spotify.com"
    return "\n".join(advice) + f"\n\n🎧 Relax with: {playlist}"

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="🌷 MindEase 2.0", page_icon="🌸", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#8B5CF6;'>🌸 MindEase 2.0 🌸</h1>"
    "<p style='text-align:center; font-size:18px;'>Your AI Therapist & Wellness Companion</p>",
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["💬 General Companion", "🌼 Women's Companion"])

# -------- TAB 1: EMOTIONAL SUPPORT --------
with tab1:
    st.markdown("### 💖 How are you feeling today?")
    text_input = st.text_area("Type your feelings here:", placeholder="I'm feeling stressed today...")
    chat_history = st.session_state.get("chat_history", [])

    if st.button("✨ Analyze & Chat"):
        mood = analyze_text(text_input)
        empathy = reply_with_empathy(text_input, mood, chat_history)
        playlist = spotify_playlist(mood)
        response = f"**Emotion:** {mood}\n\n{empathy}\n\n🎵 Playlist: {playlist or 'Not found'}"
        st.write(response)
        audio_file = tts(response)
        if audio_file:
            st.audio(audio_file)
        chat_history.append((text_input, response))
        st.session_state["chat_history"] = chat_history
        save_chat(text_input, response, mood)

    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
        st.success("Chat cleared!")

    if chat_history:
        st.markdown("### 🗨️ Conversation History")
        for user, bot in chat_history[-5:]:
            st.markdown(f"**You:** {user}")
            st.markdown(f"**MindEase:** {bot}")
            st.markdown("---")

# -------- TAB 2: WOMEN'S COMPANION --------
with tab2:
    st.markdown("### 🌿 Track your cycle & get wellness tips 🌙")
    flow = st.selectbox("🩸 Blood color", ["Bright Red", "Dark", "Brown", "Pink"])
    cramps = st.selectbox("💢 Cramps level", ["Mild", "Moderate", "Severe"])
    craving = st.selectbox("🍰 Cravings", ["Chocolate", "Salty", "Fried", "None"])

    if st.button("💗 Get My Tips"):
        result = women_health(flow, cramps, craving)
        st.text_area("🌼 Personalized Advice", value=result, height=200)

st.markdown("<br><p style='text-align:center; color:#888;'>Made with 💜 by MindEase</p>", unsafe_allow_html=True)
