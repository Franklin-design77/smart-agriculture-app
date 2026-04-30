import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("Crop_recommendation.csv")

# Separate features and target
X = data.drop("label", axis=1)
y = data["label"]

# Create and train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Prediction function
def predict_crop(N, P, K, temp, humidity, ph, rainfall):
    input_data = [[N, P, K, temp, humidity, ph, rainfall]]
    prediction = model.predict(input_data)
    return prediction[0]