Hi! 👋
This is made by faslu rahman, its my custom trained AI model project.
Hope this readme file guide you to the complete installations and steps to create a nutrition calculato by your own.


🍏 AI Food Nutrition Calculator
This project is a mobile application built with React Native that allows users to take a picture of a fruit or vegetable. The app uses a custom-trained AI model to identify the food and then fetches its nutritional information from the USDA API.

Technologies Used
------------------------
Backend: Python, Flask, TensorFlow/Keras, OpenCV, Requests

AI Model: Transfer learning with MobileNetV2

Frontend: React Native with Expo Go

APIs: USDA FoodData Central API

Testing: Postman

------------------------------------------------------------------------------------------------------------

🚀 How to Build This Project from Scratch
Follow these steps to set up and run the project on your local machine.

Part 1: Setting Up the Python Backend & AI Model
This part involves training the AI model to recognize food and setting up a server to handle requests from the mobile app.

Step 1: Set Up the Python Environment
-------------------------------------
Open your terminal and create a project folder.

Bash

mkdir Food-Tracker-Project
cd Food-Tracker-Project
Create a Python virtual environment.

On macOS/Linux: python3 -m venv venv

On Windows: python -m venv venv

Activate the environment.

On macOS/Linux: source venv/bin/activate

On Windows: venv\Scripts\activate

Install the necessary Python libraries.

Bash

pip install tensorflow opencv-python Pillow Flask requests

Step 2: Download the Dataset
--------------------------------
Download the lightweight "Fruits and Vegetables Image Recognition Dataset" from Kaggle: Download Link.

Unzip the file and place the contents into your project directory. Your folder should contain train, validation, and test sub-folders.

Step 3: Train the AI Model
--------------------------
Create a file named train.py in your project folder.

Copy the training code into train.py. Remember to update the base_dir variable to point to your dataset's location.

Run the training script from your terminal:

Bash

python train.py
This will take some time. Once finished, a new file named food_model_light.h5 will be created. This is your trained AI model.

Step 4: Create the Backend API
------------------------------
Create a file named app.py.

Sign up for a free USDA API key here: USDA API Key Signup.

Copy the API server code into app.py. Remember to update the TRAIN_DIR path and paste your USDA_API_KEY into the script.

This API loads your trained model and fetches nutrition data.

-------------------------------------------------------------------------------------------------------------

Part 2: Setting Up the React Native Frontend
---------------------------------------------------------------------
This part involves creating the mobile app that the user will interact with.

Step 1: Create the Expo Project
---------------------------------
Open a new terminal window (keep the backend terminal separate).

Create a new React Native Expo app.

Bash

npx create-expo-app NutritionApp
Navigate into the new app directory.

Bash

cd NutritionApp
Install the required packages.

Bash

npx expo install expo-image-picker axios

Step 2: Add the App Code
-------------------------
Open the NutritionApp folder in your code editor.

The new Expo version uses a file-based router. The main screen's code goes into app/(tabs)/index.tsx.

Open app/(tabs)/index.tsx, delete all existing code, and paste the frontend code provided in our conversation.

Step 3: Connect the App to the Backend
---------------------------------------
Find your computer's local IP address.

On Windows: Open Command Prompt and type ipconfig. Find the "IPv4 Address" under your Wi-Fi adapter.

On macOS: Open Terminal and type ifconfig | grep "inet ".

In app/(tabs)/index.tsx, find the API_URL constant and replace the placeholder with your IP address and the port 5000.

JavaScript

// Example
const API_URL = 'http://192.168.1.10:5000/predict';
✅ How to Run the Project
To run the full application, you need to have both the backend server and the frontend app running simultaneously.

1. Run the Backend Server

Open the terminal for your Python project (Food-Tracker-Project).

Make sure your virtual environment is active.

Run the Flask server:

Bash
-----------------------------
flask run --host=0.0.0.0    | use this command in terminal for run the flask server on all network
-----------------------------

Keep this terminal running.

2. Run the Frontend App

Open the terminal for your React Native project (NutritionApp).

Start the Expo development server:

Bash

npx expo start
A QR code will appear. Download the Expo Go app on your phone and scan the QR code.

Ensure your phone and computer are on the same Wi-Fi network.

Your app is now running! You can select an image and get an AI-powered nutrition analysis.