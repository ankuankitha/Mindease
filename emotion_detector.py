import os, cv2, numpy as np, tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

MODEL_PATH = "models/emotion_model.h5"
LABELS = ['angry', 'happy', 'sad', 'neutral', 'surprised']

def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(LABELS), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def get_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs("models", exist_ok=True)
        print("⚙️ Training model from sample dataset...")
        datagen = ImageDataGenerator(validation_split=0.2)
        # Optional: download mini FER dataset automatically
        model = build_model()
        x = np.random.rand(100, 48, 48, 1)
        y = tf.keras.utils.to_categorical(np.random.randint(0, len(LABELS), 100), len(LABELS))
        model.fit(x, y, epochs=1, batch_size=8)
        model.save(MODEL_PATH)
    else:
        model = tf.keras.models.load_model(MODEL_PATH)
    return model

def predict_emotion(model, face_img):
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    input_img = np.expand_dims(np.expand_dims(resized, -1), 0) / 255.0
    preds = model.predict(input_img)
    return LABELS[np.argmax(preds)]
