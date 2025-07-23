import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the CSV
df = pd.read_csv("player_training_data.csv")
df.dropna(inplace=True)

# Encode actions
le = LabelEncoder()
df["action_encoded"] = le.fit_transform(df["action"])

# Use all 6 features
features = df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
labels = df["action_encoded"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

# Save model and label encoder
joblib.dump(model, "player_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ Model trained and saved with 6 features.")
