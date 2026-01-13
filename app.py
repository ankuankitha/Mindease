import streamlit as st

st.set_page_config(page_title="MindEase AI", layout="centered")

st.title("🧠 MindEase AI Companion")
st.caption("Refurbished Streamlit Edition – Guaranteed Working")

# ---------------- Emotion Detection ----------------
st.subheader("😊 Emotion Detection")

emotion = st.selectbox(
    "How are you feeling today?",
    ["Happy", "Sad", "Angry", "Relaxed", "Stressed", "Neutral"]
)

st.success(f"Detected Emotion: {emotion}")

# ---------------- Chatbot ----------------
st.subheader("💬 Mental Health Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user = st.text_input("You:")

def bot_reply(msg):
    msg = msg.lower()
    if "sad" in msg:
        return "I'm here for you. You are not alone 💙"
    if "happy" in msg:
        return "That's wonderful! Keep smiling 🌸"
    if "stress" in msg:
        return "Take a deep breath. Everything will be okay."
    if "angry" in msg:
        return "It's okay to feel angry sometimes. Let's calm down together."
    if "hi" in msg or "hello" in msg:
        return "Hello! I'm your MindEase assistant 😊"
    return "Tell me more. I'm listening."

if st.button("Send"):
    if user:
        st.session_state.chat.append(("You", user))
        st.session_state.chat.append(("Bot", bot_reply(user)))

for s, m in st.session_state.chat:
    st.write(f"**{s}:** {m}")

# ---------------- Music Suggestions ----------------
st.subheader("🎵 Mood Based Music Suggestions")

songs = {
    "Happy": ["Happy - Pharrell Williams", "Good Time"],
    "Sad": ["Let Her Go", "Fix You"],
    "Angry": ["Believer", "Demons"],
    "Relaxed": ["River Flows In You", "Peaceful Guitar"],
    "Stressed": ["Weightless", "Calm Piano"],
    "Neutral": ["Perfect", "Memories"]
}

st.write("Recommended Songs:")
for s in songs[emotion]:
    st.write("🎶", s)

# ---------------- Footer ----------------
st.markdown("---")
st.info("MindEase Refurbished Streamlit Version – Runs without dependency errors.")
