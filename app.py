import streamlit as st

st.set_page_config(page_title="MindEase", layout="centered")

st.title("🧠 MindEase AI Companion")
st.success("App started successfully!")

st.subheader("😊 Emotion Detection")
emotion = st.selectbox(
    "How are you feeling?",
    ["Happy", "Sad", "Angry", "Relaxed", "Stressed", "Neutral"]
)
st.write("Detected Emotion:", emotion)

st.subheader("💬 Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user = st.text_input("You:")

def reply(msg):
    msg = msg.lower()
    if "sad" in msg:
        return "I'm here for you 💙"
    if "happy" in msg:
        return "That's great! 🌸"
    if "stress" in msg:
        return "Take a deep breath. You are okay."
    return "Tell me more."

if st.button("Send"):
    if user:
        st.session_state.chat.append(("You", user))
        st.session_state.chat.append(("Bot", reply(user)))

for s, m in st.session_state.chat:
    st.write(f"**{s}:** {m}")
