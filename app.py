import streamlit as st
import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from PIL import Image
import tempfile
import os

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MindEase - Emotion & Music",
    page_icon="🎧",
    layout="wide"
)

# --- SPOTIFY AUTH ---
SPOTIFY_CLIENT_ID = "ceb612b54e414622b7bbf9e1454f6841"
SPOTIFY_CLIENT_SECRET = "92416ba62edb46879b47dcc2ff2f5387"

@st.cache_resource
def get_spotify_client():
    """Initialize Spotify client with caching"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        return sp
    except Exception as e:
        st.error(f"Spotify initialization failed: {e}")
        return None

sp = get_spotify_client()

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .emotion-box {
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .stAudio {
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<p class="main-header">🎧 MindEase — AI Emotion & Music Companion</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/brain.png", width=100)
    st.title("Navigation")
    choice = st.radio("Choose Mode", ["🎭 Emotion Detection", "👩‍⚕️ Women's Health", "ℹ️ About"])
    
    st.markdown("---")
    st.markdown("### 🎯 How it works")
    st.info("""
    1. Upload your photo
    2. AI analyzes your emotion
    3. Get personalized music
    4. Track your mood journey
    """)

# --- EMOTION DETECTION ---
if choice == "🎭 Emotion Detection":
    st.subheader("📸 Upload an image for emotion detection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Save temporarily
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            tfile.write(uploaded_file.read())
            tfile.close()
            
            # Load and display image
            img = cv2.imread(tfile.name)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, caption="Uploaded Image", use_column_width=True)
            
    with col2:
        if uploaded_file is not None:
            # --- FACE EMOTION ANALYSIS ---
            with st.spinner("🔍 Analyzing emotion..."):
                try:
                    result = DeepFace.analyze(
                        img_path=tfile.name, 
                        actions=['emotion'], 
                        enforce_detection=False,
                        silent=True
                    )
                    
                    # Handle both list and dict results
                    if isinstance(result, list):
                        result = result[0]
                    
                    dominant_emotion = result['dominant_emotion']
                    emotion_scores = result['emotion']
                    
                    # Display dominant emotion
                    st.markdown(f'<div class="emotion-box">😊 {dominant_emotion.capitalize()}</div>', 
                              unsafe_allow_html=True)
                    
                    # Show emotion breakdown
                    st.subheader("📊 Emotion Analysis")
                    for emotion, score in sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True):
                        st.progress(score / 100, text=f"{emotion.capitalize()}: {score:.1f}%")
                    
                    # --- MUSIC RECOMMENDATION ---
                    st.markdown("---")
                    st.subheader("🎵 Personalized Music for Your Mood")
                    
                    emotion_to_query = {
                        "happy": "happy upbeat",
                        "sad": "healing calm sad",
                        "angry": "calm meditation",
                        "fear": "peaceful ambient",
                        "disgust": "uplifting positive",
                        "surprise": "energetic dance",
                        "neutral": "chill focus"
                    }
                    
                    query = emotion_to_query.get(dominant_emotion, "chill")
                    
                    if sp:
                        try:
                            results = sp.search(q=query, type="track", limit=5)
                            
                            for i, track in enumerate(results["tracks"]["items"], 1):
                                with st.container():
                                    st.markdown(f"**{i}. {track['name']}**")
                                    st.caption(f"by {', '.join([artist['name'] for artist in track['artists']])}")
                                    
                                    if track.get("preview_url"):
                                        st.audio(track["preview_url"])
                                    else:
                                        st.warning("Preview not available")
                                    
                                    st.markdown(f"[🎧 Listen on Spotify]({track['external_urls']['spotify']})")
                                    st.markdown("---")
                        except Exception as e:
                            st.error(f"Could not fetch music: {e}")
                    
                    # Clean up temp file
                    os.unlink(tfile.name)
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing image: {str(e)}")
                    st.info("💡 Try uploading a clearer image with a visible face")
                    if os.path.exists(tfile.name):
                        os.unlink(tfile.name)

# --- WOMEN'S HEALTH ---
elif choice == "👩‍⚕️ Women's Health":
    st.subheader("🌸 Women's Wellness Companion")
    st.markdown("Track your menstrual cycle and get personalized health tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        flow_color = st.selectbox("🩸 Flow Color", 
                                  ["Bright Red", "Dark Red", "Brown", "Pink", "Light Pink"])
        cramp_level = st.select_slider("💢 Cramp Intensity", 
                                       options=["None", "Mild", "Moderate", "Severe", "Extreme"])
    
    with col2:
        cravings = st.multiselect("🍫 Cravings", 
                                 ["Chocolate", "Salty Snacks", "Sweet Foods", "Fried Foods", "None"])
        mood = st.select_slider("😊 Mood Level", 
                               options=["Very Low", "Low", "Neutral", "Good", "Excellent"])
    
    if st.button("Get Personalized Advice", type="primary"):
        st.markdown("### 💡 Your Wellness Plan")
        
        advice = []
        
        # Flow color advice
        if flow_color in ["Bright Red", "Dark Red"]:
            advice.append("✅ **Flow**: Your flow appears healthy. Stay hydrated and maintain iron intake.")
        elif flow_color == "Brown":
            advice.append("🟤 **Flow**: Brown blood is old blood. Try ginger tea and light stretching.")
        elif flow_color in ["Pink", "Light Pink"]:
            advice.append("🩷 **Flow**: Light flow might indicate low iron. Include spinach, lentils, and beetroot.")
        
        # Cramp advice
        if cramp_level in ["Severe", "Extreme"]:
            advice.append("🔥 **Cramps**: Severe pain detected. Use heat therapy, take magnesium supplements, and practice deep breathing. Consider consulting a doctor.")
        elif cramp_level in ["Moderate", "Mild"]:
            advice.append("💆 **Cramps**: Moderate discomfort. Try yoga, warm baths, and chamomile tea.")
        
        # Craving advice
        if "Chocolate" in cravings:
            advice.append("🍫 **Cravings**: Chocolate craving indicates magnesium need. Choose dark chocolate (70%+ cocoa).")
        if "Salty Snacks" in cravings:
            advice.append("🥥 **Cravings**: Salt craving suggests electrolyte imbalance. Drink coconut water and eat bananas.")
        
        # Mood-based music
        if mood in ["Very Low", "Low"]:
            advice.append("🎵 **Mood Support**: You deserve care. Listen to calming music and practice self-compassion.")
            if sp:
                results = sp.search(q="healing meditation calm", type="playlist", limit=1)
                if results["playlists"]["items"]:
                    playlist = results["playlists"]["items"][0]
                    st.markdown(f"[🎧 Recommended Playlist: {playlist['name']}]({playlist['external_urls']['spotify']})")
        
        for tip in advice:
            st.success(tip)
        
        # General tips
        st.info("""
        **General Wellness Tips:**
        - Stay hydrated (8-10 glasses of water daily)
        - Light exercise (walking, yoga)
        - Adequate sleep (7-8 hours)
        - Balanced diet with iron and magnesium
        - Track your cycle for pattern recognition
        """)

# --- ABOUT ---
elif choice == "ℹ️ About":
    st.subheader("🤖 About MindEase")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What is MindEase?
        
        MindEase is an AI-powered mental health companion that:
        - Detects emotions from facial expressions
        - Recommends personalized music therapy
        - Provides women's health tracking
        - Offers empathetic support
        
        ### 🔬 Technology Stack
        
        - **DeepFace**: Advanced facial emotion recognition
        - **Spotify API**: Curated music recommendations
        - **Streamlit**: Interactive web interface
        - **OpenCV**: Image processing
        
        ### 🎵 Emotion-Music Mapping
        
        | Emotion | Music Type |
        |---------|-----------|
        | Happy | Upbeat Pop |
        | Sad | Healing Acoustic |
        | Angry | Calming Meditation |
        | Fear | Peaceful Ambient |
        | Neutral | Focus Chill |
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Features
        
        ✅ Real-time emotion detection  
        ✅ AI-powered music therapy  
        ✅ Women's health companion  
        ✅ Privacy-focused (no data stored)  
        ✅ Free and open-source  
        
        ### 🔒 Privacy & Safety
        
        - Images processed locally
        - No data storage or tracking
        - Secure Spotify integration
        - Not a replacement for professional help
        
        ### ⚠️ Important Notice
        
        MindEase is a supportive tool, **not medical advice**.
        
        If you're experiencing:
        - Severe depression
        - Suicidal thoughts
        - Mental health crisis
        
        **Please contact:**
        - Emergency: 911 (US) / 112 (EU)
        - Crisis Helpline: 988 (US)
        - Mental health professional
        
        ### 👨‍💻 Developer
        
        Built with ❤️ for mental health awareness
        
        **Tech Stack:** Python • Streamlit • DeepFace • Spotipy
        """)
    
    st.markdown("---")
    st.success("💚 Remember: It's okay to not be okay. Seeking help is a sign of strength.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🎧 MindEase v2.0 | Made with 💜 for Mental Health | Not medical advice</p>
    <p style='font-size: 0.8rem;'>If in crisis, call 988 (US) or contact local emergency services</p>
</div>
""", unsafe_allow_html=True)
