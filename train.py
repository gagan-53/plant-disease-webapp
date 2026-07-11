"""
Plant disease CNN trainer.

Mirrors the methodology from CNNSem5ProjectPlantDiseaseImageClassification.ipynb:
  - 128x128 RGB inputs, normalized to [0,1]
  - 80/20 train/test split (random_state=42)
  - Sequential CNN: Conv(32) -> Pool -> Conv(64) -> Pool -> Conv(128) -> Pool
                   -> Flatten -> Dense(128, relu) -> Dropout(0.5) -> Dense(N, softmax)
  - Adam optimizer, categorical cross-entropy loss
  - ImageDataGenerator augmentation (rotation, zoom, shifts, shear, hflip)
  - 20 epochs, batch size 32

Usage:
    python train.py --data-dir /path/to/PlantVillage/color
"""

import argparse
import json
import os

import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import (
    Conv2D, Dense, Dropout, Flatten, Input, MaxPooling2D,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

IMG_SIZE = 128
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")


def load_data(data_dir, categories):
    data = []
    for category in categories:
        path = os.path.join(data_dir, category)
        if not os.path.isdir(path):
            continue
        class_num = categories.index(category)
        for img in os.listdir(path):
            if not (img.lower().endswith(".jpg") or img.lower().endswith(".png") or img.lower().endswith(".jpeg")):
                continue
            try:
                img_array = cv2.imread(os.path.join(path, img))
                if img_array is None:
                    continue
                resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                # cv2 reads in BGR; convert to RGB so train/inference use the same channel order
                resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                data.append([resized, class_num])
            except Exception as e:
                print(f"Error processing {img}: {e}")
    return data


def build_model(num_classes):
    model = Sequential()
    model.add(Input(shape=(IMG_SIZE, IMG_SIZE, 3)))
    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True,
                        help="Path to PlantVillage color directory (one folder per class).")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-per-class", type=int, default=0,
                        help="Cap images per class for fast experiments. 0 = use all.")
    args = parser.parse_args()

    os.makedirs(MODEL_DIR, exist_ok=True)

    categories = sorted([
        d for d in os.listdir(args.data_dir)
        if os.path.isdir(os.path.join(args.data_dir, d))
    ])
    print(f"Found {len(categories)} classes in {args.data_dir}")

    data = load_data(args.data_dir, categories)
    if args.max_per_class > 0:
        from collections import defaultdict
        bucketed = defaultdict(list)
        for x, y in data:
            bucketed[y].append([x, y])
        capped = []
        for y, items in bucketed.items():
            capped.extend(items[: args.max_per_class])
        data = capped

    np.random.seed(42)
    np.random.shuffle(data)

    X = np.array([d[0] for d in data]).reshape(-1, IMG_SIZE, IMG_SIZE, 3).astype("float32")
    y = np.array([d[1] for d in data])
    X /= 255.0
    y = to_categorical(y, num_classes=len(categories))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train: {X_train.shape}  Test: {X_test.shape}")

    datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    datagen.fit(X_train)

    model = build_model(len(categories))
    model.summary()

    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=args.batch_size),
        epochs=args.epochs,
        validation_data=(X_test, y_test),
    )

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {test_acc * 100:.2f}%")

    model_path = os.path.join(MODEL_DIR, "plant_disease_model.h5")
    model.save(model_path)
    print(f"Saved model -> {model_path}")

    classes_path = os.path.join(MODEL_DIR, "class_names.json")
    with open(classes_path, "w") as f:
        json.dump(categories, f, indent=2)
    print(f"Saved class names -> {classes_path}")

    history_path = os.path.join(MODEL_DIR, "history.json")
    with open(history_path, "w") as f:
        json.dump({k: [float(v) for v in vs] for k, vs in history.history.items()}, f, indent=2)
    print(f"Saved history -> {history_path}")


if __name__ == "__main__":
    main()
