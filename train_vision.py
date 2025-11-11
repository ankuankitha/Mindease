import tensorflow as tf
import os, json
from pathlib import Path

def make_datasets(root):
    ds_train = tf.keras.preprocessing.image_dataset_from_directory(
        root, image_size=(224,224), validation_split=0.2, subset="training", seed=42
    )
    ds_val = tf.keras.preprocessing.image_dataset_from_directory(
        root, image_size=(224,224), validation_split=0.2, subset="validation", seed=42
    )
    return ds_train, ds_val, ds_train.class_names

def build_model(classes):
    base = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
    base.trainable = False
    x = tf.keras.Sequential([
        tf.keras.layers.Input((224,224,3)),
        tf.keras.layers.Rescaling(1./255),
        base,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(len(classes), activation="softmax")
    ])
    x.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return x

if __name__ == "__main__":
    ds_train, ds_val, classes = make_datasets("dataset")
    model = build_model(classes)
    model.fit(ds_train, validation_data=ds_val, epochs=10)
    os.makedirs("models", exist_ok=True)
    model.save("models/vision_emotion.h5")
    json.dump(classes, open("models/classes.json", "w"))
    print("✅ Model and class labels saved to models/")
