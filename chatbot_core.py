def generate_response(text):
    if not text:
        return "I'm listening. How are you feeling?"
    text = text.lower()
    if "sad" in text:
        return "Remember, it's okay to feel sad. Want to listen to soothing music?"
    if "angry" in text:
        return "Try breathing exercises or calm rock music."
    if "happy" in text:
        return "That's wonderful! Would you like to share what's making you smile?"
    return "I'm here with you. Tell me more."
