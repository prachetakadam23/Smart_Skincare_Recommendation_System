import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


DATASET_PATH ="../datasets/skin_concerns"
print("Dataset exists:", os.path.exists(DATASET_PATH))
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 15

CLASSES = ["dryness", "pigmentation", "acne", "wrinkles", "pores", "dark_spots", "blackheads"]

print("📂 Loading dataset...")

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

print("✅ Dataset loaded")

# ===========================
# CNN Model
# ===========================

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE,IMG_SIZE,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(len(CLASSES), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ===========================
# Train
# ===========================

print("🚀 Training started...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ===========================
# Save model
# ===========================

os.makedirs("model", exist_ok=True)
model.save("model/skin_concerns_model.h5")
print("✅ Skin concern CNN model saved successfully")

