# app.py
"""
MindEase 2.0 — Your AI Friend Therapist & Women's Companion
------------------------------------------------------------
Beautiful UI + Spotify + Empathetic Chat + Women's Health Tips
"""

import os, random, csv
from datetime import datetime
import gradio as gr
from deepface import DeepFace
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3

# ---------- Spotify credentials ----------
SPOTIFY_CREDS = {
    "client_id": "ceb612b54e414622b7bbf9e1454f6841",
    "client_secret": "92416ba62edb46879b47dcc2ff2f5387",
    "redirect_uri": "http://127.0.0.1:8000/callback"
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
try:
    emo_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    print("✅ Emotion model loaded")
except Exception as e:
    print("⚠️ Emotion model failed:", e)
    emo_model = None

try:
    chat_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    print("✅ Chat model loaded")
except Exception as e:
    print("⚠️ Chat model failed:", e)
    chat_model = None

# ---------- Helpers ----------
def analyze_face(image):
    try:
        if image is None:
            return "neutral"
        result = DeepFace.analyze(img_path=image, actions=["emotion"], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        return result.get("dominant_emotion", "neutral")
    except Exception:
        return "neutral"

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
    output = chat_model(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)[0]["generated_text"]
    return output.split("Bot:")[-1].strip()

def save_chat(user, bot, mood):
    with open("chat_history.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user, bot, mood])

# ---------- Women’s Companion ----------
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

# ---------- Main ----------
def process_input(image, text, history):
    history = history or []
    face_emo = analyze_face(image)
    text_emo = analyze_text(text)
    mood = text_emo if text_emo != "neutral" else face_emo
    playlist = spotify_playlist(mood)
    empathy = reply_with_empathy(text, mood, history)
    message = f"**Emotion:** {mood}\n{empathy}\n\n🎵 Playlist: {playlist or 'Not found'}"
    audio = tts(message)
    history.append((text, message))
    save_chat(text, message, mood)
    return history, history, audio

# ---------- UI ----------
custom_css = """
body {
    background: linear-gradient(135deg, #fdeff9, #ecf0ff);
}
.gradio-container {
    font-family: 'Poppins', sans-serif;
}
button {
    border-radius: 12px !important;
    font-weight: 600;
}
"""

with gr.Blocks(css=custom_css, title="🌷 MindEase 2.0") as demo:
    gr.Markdown(
        "<h1 style='text-align:center; color:#8B5CF6;'>🌸 MindEase 2.0 🌸</h1>"
        "<p style='text-align:center; font-size:18px;'>Your AI Therapist & Wellness Companion</p>"
    )

    with gr.Tab("💬 General Companion"):
        img = gr.Image(label="📸 Upload or Capture Face", type="numpy")
        txt = gr.Textbox(label="💖 Tell me how you feel", placeholder="I'm feeling stressed today...", lines=2)
        chat = gr.Chatbot(label="MazaBot — Your Empathy Partner", height=400, bubble_full_width=False)
        audio = gr.Audio(label="🎧 Voice Response", type="filepath")
        state = gr.State([])
        btn = gr.Button("✨ Analyze & Chat", variant="primary")
        clr = gr.Button("🧹 Clear Chat")
        btn.click(process_input, [img, txt, state], [chat, state, audio])
        clr.click(lambda: ([], [], None), None, [chat, state, audio])

    with gr.Tab("🌼 Women’s Companion"):
        gr.Markdown("<h3>Track your cycle & get mood-based self-care tips 🌙</h3>")
        flow = gr.Dropdown(["Bright Red", "Dark", "Brown", "Pink"], label="🩸 Blood color")
        cramps = gr.Dropdown(["Mild", "Moderate", "Severe"], label="💢 Cramps level")
        craving = gr.Dropdown(["Chocolate", "Salty", "Fried", "None"], label="🍰 Cravings")
        out = gr.Textbox(label="🌿 Personalized Wellness Advice", lines=7)
        sub = gr.Button("💗 Get My Tips")
        sub.click(women_health, [flow, cramps, craving], out)

if __name__ == "__main__":
    demo.launch(share=True)
