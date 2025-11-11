# tts_helper.py
def speak_text(text):
    """
    Try pyttsx3 (offline). If not installed/configured, this will raise an exception.
    On some Linux servers, pyttsx3 may not work; you can use gTTS to save an mp3 and play it.
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        # fallback: try gTTS (requires internet)
        try:
            from gtts import gTTS
            import tempfile, os
            t = gTTS(text)
            fd, path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            t.save(path)
            # play file: cross-platform solution is not trivial; try playsound
            try:
                from playsound import playsound
                playsound(path)
            finally:
                os.remove(path)
        except Exception as e:
            print("TTS unavailable:", e)
            raise
