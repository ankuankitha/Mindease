import os, json, tensorflow as tf, numpy as np

# --- 1️⃣ Create required folders ---
folders = ["data", "models", "dataset"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# --- 2️⃣ Create sample psychiatrists.csv if missing ---
csv_path = "data/psychiatrists.csv"
if not os.path.exists(csv_path):
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("name,phone,address,city,state,country\n")
        f.write("Dr. Asha Rao,+91-9999999999,MG Road,Bangalore,Karnataka,India\n")
        f.write("Dr. Raj Mehta,+91-8888888888,Andheri,Mumbai,Maharashtra,India\n")
        f.write("Dr. Priya Sharma,+91-7777777777,Connaught Place,New Delhi,Delhi,India\n")
    print("✅ Created data/psychiatrists.csv")

# --- 3️⃣ Create default classes.json ---
classes_path = "models/classes.json"
if not os.path.exists(classes_path):
    classes = ["angry", "happy", "sad", "neutral"]
    with open(classes_path, "w", encoding="utf-8") as f:
        json.dump(classes, f, indent=2)
    print("✅ Created models/classes.json")

# --- 4️⃣ Create dummy TensorFlow model ---
model_path = "models/vision_emotion.h5"
if not os.path.exists(model_path):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(4, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
    model.save(model_path)
    print("✅ Created dummy models/vision_emotion.h5")

# --- 5️⃣ Create sample dataset folders ---
for i, emotion in enumerate(["angry", "happy", "sad", "neutral"]):
    folder = os.path.join("dataset", str(i))
    os.makedirs(folder, exist_ok=True)

print("✅ Setup complete! All folders and sample files are ready.")
