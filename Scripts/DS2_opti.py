import pandas as pd
import numpy as np
from time import perf_counter

#---------- Définition des données d'entrée ----------#
df = pd.read_csv("data/dataset_2.csv")
df = df.dropna()
df = df[(df['price'] > 0) & (df['profit'] >= 0)]
df = df.reset_index(drop=True)
df['benefit_2y'] = df['price'] * df['profit'] / 100

actions = df.to_dict('records')
names = df['name'].to_numpy()
prices = (df['price'] * 100).round().astype(np.int32)  # prix en centimes
benefits = df['benefit_2y'].to_numpy(dtype=np.float32)
n = len(actions)
max_budget = 500
max_budget_cents = max_budget * 100

t_start = perf_counter()

# Table DP optimisée (1D)
dp = np.zeros(max_budget_cents + 1, dtype=np.float32)
keep = np.zeros((n, max_budget_cents + 1), dtype=bool)

for i in range(n):
    price = prices[i]
    benefit = benefits[i]
    for w in range(max_budget_cents, price - 1, -1):
        if dp[w - price] + benefit > dp[w]:
            dp[w] = dp[w - price] + benefit
            keep[i, w] = True

# Backtracking pour retrouver la solution optimale
w = np.argmax(dp)
selected_actions = []
for i in range(n - 1, -1, -1):
    if w >= prices[i] and keep[i, w]:
        selected_actions.append(actions[i])
        w -= prices[i]
selected_actions.reverse()

t_stop = perf_counter()

for action in selected_actions:
    print(f"{action['name']}: prix={action['price']}€, bénéfice={action['benefit_2y']:.2f}€")


total_price = sum(a['price'] for a in selected_actions)
total_benefit = sum(a['benefit_2y'] for a in selected_actions)
print(f"Prix total du bouquet d'actions: {total_price:.2f} euros")
print(f"Profit total des actions sélectionnées sur 2 ans: {total_benefit:.2f} euros")
print(f"Nombre d'actions: {len(selected_actions)}")
print(f"Temps d'exécution: {t_stop - t_start:.4f} secondes")
