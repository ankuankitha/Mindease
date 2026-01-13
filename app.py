import streamlit as st

st.set_page_config(page_title="MindEase", layout="centered")

st.title("🧠 MindEase AI Companion")

st.success("Streamlit is running successfully 🎉")

emotion = st.selectbox(
    "How are you feeling?",
    ["Happy", "Sad", "Angry", "Relaxed", "Stressed", "Neutral"]
)

st.write("Detected emotion:", emotion)

st.subheader("💬 Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user = st.text_input("You:")

def bot(msg):
    if not msg:
        return ""
    msg = msg.lower()
    if "sad" in msg:
        return "I am here for you 💙"
    if "happy" in msg:
        return "That’s wonderful 🌸"
    if "stress" in msg:
        return "Take a deep breath. You will be okay."
    return "Tell me more."

if st.button("Send"):
    st.session_state.chat.append(("You", user))
    st.session_state.chat.append(("Bot", bot(user)))

for s,m in st.session_state.chat:
    st.write(f"**{s}:** {m}")
