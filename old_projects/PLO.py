import gym
from gym import spaces
import numpy as np

class HoldemEnv(gym.Env):
    def __init__(self):
        super(HoldemEnv, self).__init__()
        
        # Define the observation space (hand strength, pot size, stack sizes, etc.)
        self.observation_space = spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)
        
        # Action space (Fold, Check/Call, Bet/Raise)
        self.action_space = spaces.Discrete(3)  # 0: Fold, 1: Call, 2: Bet/Raise
        
        # Initialize game state
        self.reset()

    def reset(self):
        # Reset the game state
        self.state = np.random.rand(10)  # Random state for demonstration
        return self.state

    def step(self, action):
        # Apply action to the game state
        done = False
        reward = 0
        
        # Simplified reward logic based on action
        if action == 0:  # Fold
            reward = -1
            done = True
        elif action == 1:  # Call
            reward = np.random.choice([0, 1])
        elif action == 2:  # Bet/Raise
            reward = np.random.choice([1, 2, -1])  # Win more or lose, for demo purposes

        # Update state (randomly for simplicity)
        self.state = np.random.rand(10)
        
        # Return updated state, reward, and done status
        return self.state, reward, done, {}

