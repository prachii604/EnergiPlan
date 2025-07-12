import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
data = pd.read_csv("dataset.csv")  # Make sure this file has correct data

# Define features and target
X = data[['temperature', 'humidity', 'cloud_cover', 'irradiance']]
y = data['solar_output']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model properly
joblib.dump(model, "solar_model.pkl")
print("Model trained and saved as solar_model.pkl")
