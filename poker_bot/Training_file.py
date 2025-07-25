import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# -----------------------
# 🎯 Train PLAYER model
# -----------------------
try:
    df = pd.read_csv("player_training_data.csv")
    df.dropna(inplace=True)

    le = LabelEncoder()
    df["action_encoded"] = le.fit_transform(df["action"])

    features = df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
    labels = df["action_encoded"]

    player_model = RandomForestClassifier(n_estimators=100, random_state=42)
    player_model.fit(features, labels)

    joblib.dump(player_model, "player_model.pkl")
    joblib.dump(le, "label_encoder.pkl")
    print("✅ Player action model trained and saved.")

    # Train player bet size model (only on raises)
    bet_df = df[(df["action"] == "raise") & (df["bet_size"] > 0)]
    if not bet_df.empty:
        bet_features = bet_df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
        bet_target = bet_df["bet_size"]
        bet_model = RandomForestRegressor(n_estimators=100, random_state=42)
        bet_model.fit(bet_features, bet_target)
        joblib.dump(bet_model, "bet_size_model.pkl")
        print("✅ Player bet size model trained and saved.")
    else:
        print("⚠️ Not enough player raise data to train bet size model.")
except Exception as e:
    print(f"❌ Player model training failed: {e}")

# -----------------------
# 🤖 Train BOT model
# -----------------------
try:
    bot_df = pd.read_csv("bot_training_data.csv")
    bot_df.dropna(inplace=True)

    le_bot = LabelEncoder()
    bot_df["action_encoded"] = le_bot.fit_transform(bot_df["action"])

    bot_features = bot_df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
    bot_labels = bot_df["action_encoded"]

    bot_model = RandomForestClassifier(n_estimators=100, random_state=42)
    bot_model.fit(bot_features, bot_labels)

    joblib.dump(bot_model, "bot_action_model.pkl")
    joblib.dump(le_bot, "bot_action_encoder.pkl")
    print("✅ Bot action model trained and saved.")

    # Train bot's own bet size model (only on aggressive actions)
    bet_bot_df = bot_df[bot_df["action"].isin(["bet", "raise", "bluff"]) & (bot_df["bet_size"] > 0)]
    if not bet_bot_df.empty:
        bot_bet_features = bet_bot_df[["hand_strength", "board_texture", "player_stack", "bot_stack", "pot_size", "street_id"]]
        bot_bet_target = bet_bot_df["bet_size"]
        bot_bet_model = RandomForestRegressor(n_estimators=100, random_state=42)
        bot_bet_model.fit(bot_bet_features, bot_bet_target)
        joblib.dump(bot_bet_model, "bot_bet_size_model.pkl")
        print("✅ Bot bet size model trained and saved.")
    else:
        print("⚠️ Not enough bot raise data to train bet size model.")
except Exception as e:
    print(f"❌ Bot model training failed: {e}")
