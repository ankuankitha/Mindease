import os
import tensorflow as tf
import numpy as np
import cv2, json

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

class FaceEmotionDetector:
    def __init__(self):
        self.model = tf.keras.models.load_model("models/vision_emotion.h5")
        with open("models/classes.json") as f:
            self.classes = json.load(f)

    def predict(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (48, 48))
        face = face.reshape(1, 48, 48, 1) / 255.0
        pred = self.model.predict(face, verbose=0)
        idx = np.argmax(pred)
        return self.classes[idx], float(pred[0][idx])
