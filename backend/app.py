# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import requests
# import joblib
# import numpy as np
# import os




# # Setup Flask
# app = Flask(__name__, static_folder='../frontend-p', static_url_path='')
# CORS(app)

# # Load ML model
# API_KEY = "0e2aa62cfde3cd4f7cf6e161c20cbce8"
# MODEL_PATH = os.path.join("..", "ml_model", "solar_model.pkl")
# MODEL = joblib.load(MODEL_PATH)

# # Predict route
# @app.route('/predict', methods=['GET'])
# def predict():
#     city = request.args.get('city', default='Delhi', type=str)

#     weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
#     response = requests.get(weather_url)
#     data = response.json()

#     if data.get("cod") != "200":
#         return jsonify({"error": "City not found"}), 400

#     forecast = data['list'][0]
#     temp = forecast['main']['temp']
#     humidity = forecast['main']['humidity']
#     cloud_cover = forecast['clouds']['all']
#     wind_speed = forecast['wind']['speed']
#     wind_deg = forecast['wind'].get('deg', 0)
#     irradiance = max(0, 1000 - (cloud_cover * 8))


#     input_features = np.array([[temp, humidity, cloud_cover, irradiance]])
#     prediction = MODEL.predict(input_features)[0]

#     return jsonify({
#         'city': city,
#         'temperature': temp,
#         'humidity': humidity,
#         'cloud_cover': cloud_cover,
#         'irradiance': irradiance,
#         'prediction': round(prediction, 2)
#         'wind_speed': wind_speed,
#         'wind_deg': wind_deg
#     })


# # Serve index.html
# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

# # Serve other static assets (CSS, JS, etc.)
# @app.route('/<path:path>')
# def serve_file(path):
#     return send_from_directory(app.static_folder, path)

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)






from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import joblib
import numpy as np
import os

# Setup Flask
app = Flask(__name__, static_folder='../frontend-p', static_url_path='')
CORS(app)

# Load ML model
API_KEY = "0e2aa62cfde3cd4f7cf6e161c20cbce8"  # Replace with your valid key
MODEL_PATH = os.path.join("..", "ml_model", "solar_model.pkl")
MODEL = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['GET'])
def predict():
    city = request.args.get('city', default='Delhi', type=str)
    weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    data = response.json()

    if data.get("cod") != "200":
        return jsonify({"error": "City not found"}), 400

    forecast = data['list'][0]
    temp = forecast['main']['temp']
    humidity = forecast['main']['humidity']
    cloud_cover = forecast['clouds']['all']
    wind_speed = forecast['wind']['speed']
    wind_deg = forecast['wind'].get('deg', 0)
    irradiance = max(0, 1000 - (cloud_cover * 8))

    input_features = np.array([[temp, humidity, cloud_cover, irradiance]])
    prediction = MODEL.predict(input_features)[0]

    return jsonify({
        'city': city,
        'temperature': temp,
        'humidity': humidity,
        'cloud_cover': cloud_cover,
        'irradiance': irradiance,
        'prediction': round(prediction, 2),
        'wind_speed': wind_speed,
        'wind_deg': wind_deg
    })

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
