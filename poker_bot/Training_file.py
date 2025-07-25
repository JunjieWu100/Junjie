import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load and clean the data
df = pd.read_csv("player_training_data.csv")
df.dropna(inplace=True)

# -----------------------
# 🎯 Train action classifier
# -----------------------
le = LabelEncoder()
df["action_encoded"] = le.fit_transform(df["action"])

features = df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
labels = df["action_encoded"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

joblib.dump(model, "player_model.pkl")
joblib.dump(le, "label_encoder.pkl")
print("✅ Action model trained and saved.")

# -----------------------
# 🔥 Train bet size regressor (only on 'raise' actions)
# -----------------------
bet_df = df[(df["action"] == "raise") & (df["bet_size"] > 0)]

if not bet_df.empty:
    bet_features = bet_df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
    bet_target = bet_df["bet_size"]

    bet_model = RandomForestRegressor(n_estimators=100, random_state=42)
    bet_model.fit(bet_features, bet_target)

    joblib.dump(bet_model, "bet_size_model.pkl")
    print("✅ Bet size model trained and saved.")
else:
    print("⚠️ Not enough raise data to train bet size model.")
