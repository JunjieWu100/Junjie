# 📦 Install XGBoost
!pip install xgboost

# 📚 Imports
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 🎲 Set seed for reproducibility
SEED = 42
np.random.seed(SEED)

# 🔧 1. Generate Simulated Training Data
def generate_data(n=300):
    rows = []
    for _ in range(n):
        elo_A = np.random.randint(1500, 1600)
        elo_B = np.random.randint(1500, 1600)
        home = np.random.choice([0, 1])

        atk_A = np.random.normal(70, 5)
        def_B = np.random.normal(70, 5)
        gk_B  = np.random.normal(70, 3)

        atk_B = np.random.normal(70, 5)
        def_A = np.random.normal(70, 5)
        gk_A  = np.random.normal(70, 3)

        # Team stats (simulated)
        stats_A = {
            'shots': np.random.uniform(8, 28),
            'possession': np.random.uniform(40, 65),
            'xG': np.random.uniform(2.0, 5.0)
        }
        stats_B = {
            'shots': np.random.uniform(8, 28),
            'possession': np.random.uniform(40, 65),
            'xG': np.random.uniform(2.0, 5.0)
        }

        # Simulated goal generation
        elo_diff = elo_A - elo_B
        lambda_A = stats_A['xG'] + 0.01 * elo_diff + 0.03 * (atk_A - def_B) - 0.01 * (gk_B - 70)
        lambda_B = stats_B['xG'] - 0.01 * elo_diff + 0.03 * (atk_B - def_A) - 0.01 * (gk_A - 70)

        goals_A = np.random.poisson(max(lambda_A, 0.2))
        goals_B = np.random.poisson(max(lambda_B, 0.2))

        rows.append([
            elo_A, elo_B, elo_diff, home,
            atk_A, def_B, gk_B,
            stats_A['shots'], stats_A['possession'], stats_A['xG'],
            goals_A,
            atk_B, def_A, gk_A,
            stats_B['shots'], stats_B['possession'], stats_B['xG'],
            goals_B
        ])
    
    cols = [
        'elo_A', 'elo_B', 'elo_diff', 'home',
        'atk_A', 'def_B', 'gk_B',
        'shots_A', 'poss_A', 'xG_A',
        'goals_A',
        'atk_B', 'def_A', 'gk_A',
        'shots_B', 'poss_B', 'xG_B',
        'goals_B'
    ]
    return pd.DataFrame(rows, columns=cols)

df = generate_data()

# 🧠 2. Define Features and Train Models
features_A = ['elo_A', 'elo_B', 'elo_diff', 'home',
              'atk_A', 'def_B', 'gk_B',
              'shots_A', 'poss_A', 'xG_A']

features_B = ['elo_A', 'elo_B', 'elo_diff', 'home',
              'atk_B', 'def_A', 'gk_A',
              'shots_B', 'poss_B', 'xG_B']

X_A = df[features_A]
y_A = df['goals_A']
X_B = df[features_B]
y_B = df['goals_B']

X_A_train, X_A_test, y_A_train, y_A_test = train_test_split(X_A, y_A, test_size=0.2, random_state=SEED)
X_B_train, X_B_test, y_B_train, y_B_test = train_test_split(X_B, y_B, test_size=0.2, random_state=SEED)

model_A = XGBRegressor(random_state=SEED)
model_B = XGBRegressor(random_state=SEED)
model_A.fit(X_A_train, y_A_train)
model_B.fit(X_B_train, y_B_train)

# 📊 3. Evaluate Models
rmse_A = np.sqrt(mean_squared_error(y_A_test, model_A.predict(X_A_test)))
rmse_B = np.sqrt(mean_squared_error(y_B_test, model_B.predict(X_B_test)))
print(f"✅ Model A RMSE: {rmse_A:.3f} goals")
print(f"✅ Model B RMSE: {rmse_B:.3f} goals")

# ✍️ 4. INPUT DATA — Replace with real stats

# --- TEAM A INPUTS ---
team_A = {
    'elo': 1584,
    'atk': 70.0,
    'shots': 12.0,
    'poss': 53.0,
    'xG': 1.653
}

# --- TEAM B INPUTS ---
team_B = {
    'elo': 1601,
    'atk': 70.0,
    'shots': 8.0,
    'poss': 47.0,
    'xG': 1.857
}

# --- SHARED CONTEXT ---
shared = {
    'home': 1,        # 1 if Team A is home, 0 otherwise
    'def_A': 70.0,
    'def_B': 70.0,
    'gk_A': 70.0,
    'gk_B': 70.0
}

# --- Assemble DataFrames for Prediction ---

input_A = pd.DataFrame([{
    'elo_A': team_A['elo'],
    'elo_B': team_B['elo'],
    'elo_diff': team_A['elo'] - team_B['elo'],
    'home': shared['home'],
    'atk_A': team_A['atk'],
    'def_B': shared['def_B'],
    'gk_B': shared['gk_B'],
    'shots_A': team_A['shots'],
    'poss_A': team_A['poss'],
    'xG_A': team_A['xG']
}])

input_B = pd.DataFrame([{
    'elo_A': team_A['elo'],
    'elo_B': team_B['elo'],
    'elo_diff': team_A['elo'] - team_B['elo'],
    'home': shared['home'],
    'atk_B': team_B['atk'],
    'def_A': shared['def_A'],
    'gk_A': shared['gk_A'],
    'shots_B': team_B['shots'],
    'poss_B': team_B['poss'],
    'xG_B': team_B['xG']
}])


# 🔮 5. Predict Goals for Both Teams
pred_A = model_A.predict(input_A)[0]
pred_B = model_B.predict(input_B)[0]

print(f"\n⚽ Predicted goals:")
print(f"Team A: {pred_A:.2f}")
print(f"Team B: {pred_B:.2f}")
