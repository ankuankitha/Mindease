import os, json, tensorflow as tf

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def ensure_setup():
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("dataset", exist_ok=True)

    # psychiatrists.csv
    if not os.path.exists("data/psychiatrists.csv"):
        with open("data/psychiatrists.csv", "w", encoding="utf-8") as f:
            f.write("name,phone,location\n")
            f.write("Dr. Asha Rao,+91-9999999999,Bangalore\n")
            f.write("Dr. Raj Mehta,+91-8888888888,Mumbai\n")
            f.write("Dr. Priya Sharma,+91-7777777777,Delhi\n")

    # classes
    classes = ["angry", "happy", "sad", "neutral"]
    with open("models/classes.json", "w") as f:
        json.dump(classes, f)

    # model
    model_path = "models/vision_emotion.h5"
    if not os.path.exists(model_path):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(48, 48, 1)),
            tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(4, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
        model.save(model_path)
        print("✅ Dummy emotion model created.")
