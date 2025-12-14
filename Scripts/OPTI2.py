import pandas as pd
import numpy as np
from time import perf_counter
from numba import njit

#---------- Définition des données d'entrée ----------#
df = pd.read_csv("data/dataset_1.csv")
df = df.dropna()
df = df[(df['price'] > 0) & (df['profit'] >= 0)]
df = df.reset_index(drop=True)
df['benefit_2y'] = df['price'] * df['profit'] / 100

prices = (df['price'] * 100).round().astype(np.int32).to_numpy()
benefits = df['benefit_2y'].to_numpy(dtype=np.float32)
n = len(prices)
max_budget = 500
max_budget_cents = max_budget * 100

t_start = perf_counter()

@njit
def knapsack_numba(prices, benefits, n, max_budget_cents):
    dp = np.zeros(max_budget_cents + 1, dtype=np.float32)
    keep = np.zeros((n, max_budget_cents + 1), dtype=np.bool_)
    for i in range(n):
        price = prices[i]
        benefit = benefits[i]
        for w in range(max_budget_cents, price - 1, -1):
            if dp[w - price] + benefit > dp[w]:
                dp[w] = dp[w - price] + benefit
                keep[i, w] = True
    return dp, keep

dp, keep = knapsack_numba(prices, benefits, n, max_budget_cents)

# Backtracking pour retrouver la solution optimale
w = np.argmax(dp)
selected_indices = []
for i in range(n - 1, -1, -1):
    if w >= prices[i] and keep[i, w]:
        selected_indices.append(i)
        w -= prices[i]
selected_indices.reverse()

selected_actions = df.iloc[selected_indices]

t_stop = perf_counter()

for _, action in selected_actions.iterrows():
    print(f"{action['name']}: prix={action['price']}€, bénéfice={action['benefit_2y']:.2f}€")

total_price = selected_actions['price'].sum()
total_benefit = selected_actions['benefit_2y'].sum()
print(f"Prix total du bouquet d'actions: {total_price:.2f} euros")
print(f"Profit total des actions sélectionnées sur 2 ans: {total_benefit:.2f} euros")
print(f"Nombre d'actions: {len(selected_actions)}")
print(f"Temps d'exécution: {t_stop - t_start:.4f} secondes")

# Affichage standardisé pour speed_test.py
print(f"[RESULT] PRIX_TOTAL={total_price:.2f} BENEFICE_TOTAL={total_benefit:.2f} TEMPS={t_stop - t_start:.4f}")

# Affichage compatible speed_test.py (sans accent ni apostrophe)
print(f"Total price: {total_price:.2f} euros")
print(f"Total benefit: {total_benefit:.2f} euros")
print(f"Time taken: {t_stop - t_start:.4f} seconds")
