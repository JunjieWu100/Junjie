from stable_baselines3 import PPO

# Initialize the custom Hold'em environment
env = HoldemEnv()

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)  # Adjust timesteps as needed

# Save the trained model
model.save("holdem_bot")

# To load and play later:
# model = PPO.load("holdem_bot")
