import os
import io
import numpy as np
import requests 
from PIL import Image
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = 'food_model_light.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# IMPORTANT: Make sure this path is correct
TRAIN_DIR = r'D:\taining\archive/train' 
train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    shuffle=False,
    image_size=(224, 224)
)
class_names = train_dataset.class_names

# Nutrition API key (replace with your actual key) from USDA API(FoodData Central)
USDA_API_KEY = 'hIUDFdtxgQ1taHWz2mC1UFNVbydV1J5nAIGdiGxW'

def prepare_image(image_data, target_size):
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    img = img.resize(target_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        try:
            image_data = file.read()
            prepared_image = prepare_image(image_data, target_size=(224, 224))
            
            prediction = model.predict(prepared_image)
            
            predicted_class_index = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]))
            predicted_class_name = class_names[predicted_class_index]
            
            nutrition_info = {}
            
            search_response = requests.get(
                f'https://api.nal.usda.gov/fdc/v1/foods/search?query={predicted_class_name}&api_key={USDA_API_KEY}&pageSize=1'
            )
            search_data = search_response.json()
            if search_data.get('foods'):
                food_nutrients = search_data['foods'][0]['foodNutrients']
                for nutrient in food_nutrients:
                    if nutrient['nutrientName'] in ["Energy", "Protein", "Total lipid (fat)", "Carbohydrate, by difference"]:
                        name = nutrient['nutrientName'].replace(", by difference", "")
                        value = f"{nutrient.get('value', 0)} {nutrient.get('unitName', '').lower()}"
                        nutrition_info[name] = value
            
            return jsonify({
                "predicted_food": predicted_class_name,
                "confidence": f"{confidence:.2%}",
                "nutrition": nutrition_info
            })
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
if __name__ == "__main__":
    app.run(debug=True)        