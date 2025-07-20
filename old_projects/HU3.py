# Reset the environment
obs = env.reset()
done = False
total_reward = 0

while not done:
    # Predict action based on the current state
    action, _states = model.predict(obs)
    
    # Apply action in the environment
    obs, reward, done, info = env.step(action)
    total_reward += reward

    # Print current action and state
    print(f"Action: {action}, Reward: {reward}, Total Reward: {total_reward}")

print("Game finished with total reward:", total_reward)
