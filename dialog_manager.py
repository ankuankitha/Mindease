class DialogManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.step = 0
        self.emotion = None
        self.confidence = 0
        self.awaiting_user = False
        self.got_emotion = False

    def set_emotion(self, emotion, conf):
        self.emotion = emotion
        self.confidence = conf
        self.got_emotion = True

    def next_message(self):
        if not self.got_emotion:
            return "Please capture your face to detect emotion.", False
        messages = {
            "happy": "You look cheerful! Keep it up 🌞 Would you like relaxation music?",
            "sad": "You seem a bit down. It's okay — take a deep breath 🌧",
            "angry": "You appear upset. Try some deep breathing 🧘‍♀️",
            "neutral": "You seem calm. Let’s keep that balance 🌿"
        }
        return messages.get(self.emotion, "Let's talk about your day."), True
