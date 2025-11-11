import streamlit as st
import cv2
from fer import FER
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
st.title("🧠 MindEase - Emotion Detection & Music Therapy")

# -----------------------------
# SPOTIFY SETUP
# -----------------------------
try:
    SPOTIFY_CREDS = {
    "client_id": "ceb612b54e414622b7bbf9e1454f6841",
    "client_secret": "92416ba62edb46879b47dcc2ff2f5387",
    "redirect_uri": "http://127.0.0.1:8000/callback"
}

except Exception:
    st.warning("⚠️ Spotify credentials missing in Streamlit secrets. Add them first!")
    st.stop()

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CREDS["client_id"],
    client_secret=SPOTIFY_CREDS["client_secret"],
    redirect_uri=SPOTIFY_CREDS["redirect_uri"],
    scope=scope
))

# -----------------------------
# FACE EMOTION ANALYZER
# -----------------------------
detector = FER(mtcnn=True)
FRAME_WINDOW = st.image([])
run_camera = st.checkbox("🎥 Start Webcam for Emotion Detection")

emotion_detected = None

if run_camera:
    cam = cv2.VideoCapture(0)
    st.info("Webcam active! Please wait a few seconds...")
    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("⚠️ Camera not accessible.")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = detector.detect_emotions(frame_rgb)

        if results:
            emotion_detected = max(results[0]["emotions"], key=results[0]["emotions"].get)
            cv2.putText(frame_rgb, f"Emotion: {emotion_detected}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame_rgb, "Detecting...", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        FRAME_WINDOW.image(frame_rgb)
        time.sleep(0.25)
else:
    st.info("✅ Webcam stopped.")

# -----------------------------
# MUSIC RECOMMENDATION
# -----------------------------
def get_playlist_for_emotion(emotion):
    playlists = {
        "happy": "Happy Hits!",
        "sad": "Life Sucks",
        "angry": "Rock Classics",
        "neutral": "Chill Hits",
        "fear": "Peaceful Piano",
        "surprise": "Good Vibes"
    }
    query = playlists.get(emotion, "Chill Hits")
    results = spotify.search(q=query, type='playlist', limit=5)
    if results["playlists"]["items"]:
        return random.choice(results["playlists"]["items"])["external_urls"]["spotify"]
    return None

if st.button("🎵 Recommend Music"):
    if emotion_detected:
        url = get_playlist_for_emotion(emotion_detected)
        if url:
            st.success(f"Detected emotion: **{emotion_detected}**")
            st.markdown(f"[🎧 Open Playlist]({url})")
        else:
            st.warning("No playlist found.")
    else:
        st.info("Please detect an emotion first.")

# -----------------------------
# VOICE ENCOURAGEMENT
# -----------------------------
if st.button("💬 Speak Encouragement"):
    engine = pyttsx3.init()
    msg = random.choice([
        "You are doing amazing, keep it up!",
        "Take a deep breath and relax.",
        "Every challenge makes you stronger."
    ])
    st.write(msg)
    engine.say(msg)
    engine.runAndWait()
