import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyttsx3
import random
import time

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(page_title="MindEase", page_icon="🧘", layout="wide")

st.title("🧠 MindEase - Emotion Detection and Music Therapy App")

# -----------------------------
# LOAD SPOTIFY CREDENTIALS
# -----------------------------
try:
    SPOTIFY_CREDS = {
        "client_id": st.secrets[""ceb612b54e414622b7bbf9e1454f6841""],
        "client_secret": st.secrets["92416ba62edb46879b47dcc2ff2f5387"],
        "redirect_uri": st.secrets["http://127.0.0.1:8000/callback"]
    }
except Exception:
    st.warning("⚠️ Spotify credentials not found! Please add them in Streamlit Secrets.")
    st.stop()

# Spotify authorization
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CREDS["client_id"],
    client_secret=SPOTIFY_CREDS["client_secret"],
    redirect_uri=SPOTIFY_CREDS["redirect_uri"],
    scope="user-read-playback-state,user-modify-playback-state"
)
spotify = spotipy.Spotify(auth_manager=sp_oauth)

# -----------------------------
# CAMERA & EMOTION DETECTION
# -----------------------------
st.subheader("🎭 Emotion Detection")

run_camera = st.checkbox("Start Webcam")
FRAME_WINDOW = st.image([])

if run_camera:
    camera = cv2.VideoCapture(0)
    st.info("Webcam started... please wait a moment.")
    while run_camera:
        ret, frame = camera.read()
        if not ret:
            st.error("⚠️ Unable to access webcam.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            analysis = DeepFace.analyze(frame_rgb, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']
            cv2.putText(frame_rgb, dominant_emotion, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        except Exception as e:
            dominant_emotion = "neutral"
            cv2.putText(frame_rgb, "Detecting...", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        FRAME_WINDOW.image(frame_rgb)

        time.sleep(0.2)
    camera.release()
else:
    st.info("✅ Webcam stopped.")

# -----------------------------
# EMOTION → MUSIC SUGGESTION
# -----------------------------
def get_playlist_for_emotion(emotion):
    emotion_playlists = {
        "happy": "Happy Hits!",
        "sad": "Life Sucks",
        "angry": "Rock Classics",
        "neutral": "Chill Hits",
        "fear": "Peaceful Piano",
        "surprise": "Good Vibes"
    }
    query = emotion_playlists.get(emotion, "Chill Hits")
    results = spotify.search(q=query, type='playlist', limit=5)
    if results["playlists"]["items"]:
        return random.choice(results["playlists"]["items"])["external_urls"]["spotify"]
    return None

if st.button("🎵 Recommend Music"):
    emotion = "happy"  # default
    st.info("Analyzing mood and finding music...")
    url = get_playlist_for_emotion(emotion)
    if url:
        st.success(f"Your emotion is **{emotion}**. Here's a playlist for you:")
        st.markdown(f"[Open Playlist 🎧]({url})")
    else:
        st.error("Couldn't find a suitable playlist.")

# -----------------------------
# SPEECH FEEDBACK
# -----------------------------
st.subheader("🗣️ Voice Feedback")
if st.button("Speak Encouragement"):
    engine = pyttsx3.init()
    messages = [
        "You are doing great, keep going!",
        "Take a deep breath. Everything will be okay.",
        "Remember, you are stronger than you think."
    ]
    msg = random.choice(messages)
    st.write(msg)
    engine.say(msg)
    engine.runAndWait()

