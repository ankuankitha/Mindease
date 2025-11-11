import streamlit as st
import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from PIL import Image
import tempfile
import os

# --- SPOTIFY AUTH ---
SPOTIFY_CLIENT_ID = "ceb612b54e414622b7bbf9e1454f6841"
SPOTIFY_CLIENT_SECRET = "92416ba62edb46879b47dcc2ff2f5387"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# --- STREAMLIT UI ---
st.title("🎧 MindEase — Emotion & Music Recommender")

menu = ["Emotion Detection", "About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Emotion Detection":
    st.subheader("Upload an image for emotion detection")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save temporarily
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        # Load image
        img = cv2.imread(tfile.name)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, caption="Uploaded Image", use_column_width=True)

        # --- FACE EMOTION ANALYSIS ---
        with st.spinner("Analyzing emotion..."):
            try:
                result = DeepFace.analyze(img_path=tfile.name, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                st.success(f"Detected emotion: **{dominant_emotion.capitalize()}**")

                # --- MUSIC RECOMMENDATION ---
                st.subheader("🎵 Spotify Recommendations")
                emotion_to_genre = {
                    "happy": "pop",
                    "sad": "acoustic",
                    "angry": "metal",
                    "fear": "ambient",
                    "disgust": "punk",
                    "surprise": "dance",
                    "neutral": "chill"
                }
                genre = emotion_to_genre.get(dominant_emotion, "pop")

                results = sp.search(q=f"genre:{genre}", type="track", limit=5)
                for track in results["tracks"]["items"]:
                    st.write(f"**{track['name']}** by {track['artists'][0]['name']}")
                    st.audio(track["preview_url"])
            except Exception as e:
                st.error(f"Error: {e}")

elif choice == "About":
    st.markdown("""
    ### 🤖 MindEase App
    Detect emotions from facial expressions using DeepFace,  
    and get personalized Spotify music suggestions that match your mood.
    
    **Tech stack:** Streamlit · OpenCV · DeepFace · Spotipy  
    """)

