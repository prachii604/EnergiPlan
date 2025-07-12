import requests
import pandas as pd
import numpy as np
from datetime import datetime

API_KEY = "0e2aa62cfde3cd4f7cf6e161c20cbce8"

# List of diverse Indian cities
cities = [
    "Delhi", "Jaipur", "Jodhpur", "Mumbai", "Chennai", "Kolkata",
    "Hyderabad", "Ahmedabad", "Bengaluru", "Pune", "Surat",
    "Lucknow", "Bhopal", "Ranchi", "Patna", "Raipur", "Nagpur"
]

all_records = []

for city in cities:
    print(f"Fetching weather data for {city}...")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            print(f"Skipping {city}: {data.get('message')}")
            continue

        for item in data["list"]:
            dt_txt = item['dt_txt']
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            cloud = item["clouds"]["all"]
            irradiance = max(0, 1000 - cloud * 8)

            # Simulate solar output
            noise = np.random.normal(0, 30)
            solar_output = round((0.6 * irradiance) - (0.3 * cloud) + noise, 2)
            solar_output = max(0, solar_output)  # Ensure non-negative

            all_records.append({
                "datetime": dt_txt,
                "city": city,
                "temperature": temp,
                "humidity": humidity,
                "cloud_cover": cloud,
                "irradiance": irradiance,
                "solar_output": solar_output
            })
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")

# Create DataFrame and save
df = pd.DataFrame(all_records)
df.to_csv("dataset.csv", index=False)
print("✅ Dataset saved as dataset.csv")
