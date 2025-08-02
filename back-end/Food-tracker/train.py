import tensorflow as tf
import os

# --- UPDATED SECTION ---

# 1. --- DEFINE PATHS TO THE NEW DATASET ---
# Define the base path to where you extracted the dataset
base_dir = r'D:\taining\archive' # IMPORTANT: Change this path!

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Define parameters for the loader
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

# 2. --- LOAD THE DATASETS FROM THEIR FOLDERS ---
# No longer need 'validation_split' as the data is already split.
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    shuffle=True,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    validation_dir,
    shuffle=False,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# Get the class names from the training dataset
class_names = train_dataset.class_names
print(f"Found {len(class_names)} classes.")

# --- THE REST OF THE CODE IS THE SAME ---

# 3. --- CONFIGURE THE DATASET FOR PERFORMANCE ---
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
])

rescale_layer = tf.keras.layers.Rescaling(1./255)

train_dataset = train_dataset.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)
train_dataset = train_dataset.map(lambda x, y: (rescale_layer(x), y), num_parallel_calls=AUTOTUNE)
validation_dataset = validation_dataset.map(lambda x, y: (rescale_layer(x), y), num_parallel_calls=AUTOTUNE)


# 4. --- BUILD AND TRAIN THE MODEL (No changes here) ---
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
                                               include_top=False,
                                               weights='imagenet')
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

initial_epochs = 10
history = model.fit(train_dataset,
                    epochs=initial_epochs,
                    validation_data=validation_dataset)

# 5. --- SAVE THE FINAL MODEL ---
model.save('food_model_light.h5')

print("Model trained and saved as food_model_light.h5")