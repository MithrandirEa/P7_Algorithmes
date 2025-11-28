"""
Algorithme Knapsack 0/1 optimisé avec programmation dynamique
Optimisations: numpy vectorization, granularité centimes, pré-tri
"""

import pandas as pd
import numpy as np
from time import perf_counter

t_start = perf_counter()


def knapsack_01(actions, max_budget):
    """Knapsack 0/1 avec numpy pour performances maximales"""
    n = len(actions)
    budget_cents = int(max_budget * 100)
    
    # Conversion en numpy arrays pour vectorisation
    prices = np.array([int(action['price'] * 100) for action in actions], dtype=np.int32)
    benefits = np.array([action['benefit_2y'] for action in actions], dtype=np.float32)
    
    # Pré-tri par ratio benefit/price pour meilleure exploration
    ratios = benefits / (prices / 100)
    sorted_idx = np.argsort(ratios)[::-1]
    prices = prices[sorted_idx]
    benefits = benefits[sorted_idx]
    actions_sorted = [actions[i] for i in sorted_idx]
    
    # Table DP: une seule ligne (prev)
    dp = np.zeros(budget_cents + 1, dtype=np.float32)
    
    # Matrice keep compacte (bool pour économiser mémoire)
    keep = np.zeros((n + 1, budget_cents + 1), dtype=np.bool_)
    
    for i in range(n):
        price = prices[i]
        benefit = benefits[i]
        
        # Parcourir en sens inverse pour éviter le doublon
        for w in range(budget_cents, price - 1, -1):
            new_val = dp[w - price] + benefit
            if new_val > dp[w]:
                dp[w] = new_val
                keep[i + 1, w] = True
    
    # Backtracking optimisé
    selected = []
    w = budget_cents
    for i in range(n, 0, -1):
        if keep[i, w]:
            selected.append(actions_sorted[i - 1])
            w -= prices[i - 1]
    
    selected.reverse()
    return float(dp[budget_cents]), selected


df = pd.read_csv("first_search/data/dataset_1.csv")
df = df.dropna(subset=["price", "profit"])
df = df[(df["price"] > 0) & (df["profit"] > 0)]
df["benefit_2y"] = df["price"] * df["profit"] / 100

actions = df.to_dict('records')
max_benefit, selected = knapsack_01(actions, max_budget=500)

total_price = sum(action['price'] for action in selected)
total_benefit = sum(action['benefit_2y'] for action in selected)
budget_utilise_pct = (total_price / 500) * 100
rendement_global = (total_benefit / total_price * 100) if total_price > 0 else 0

print(f"Prix total du bouquet d'actions: {total_price:.2f} euros")
print(f"Budget utilisé: {budget_utilise_pct:.2f}%")
print(f"Profit total des actions sélectionnées sur 2 ans: {total_benefit:.2f} euros")
print(f"Rendement global: {rendement_global:.2f}%")
print(f"Nombre d'actions: {len(selected)}")
print("\nActions sélectionnées:")
for action in selected:
    print(f" - {action['name']:20s} - {action['price']:8.2f}€ (bénéfice : {action['benefit_2y']:8.2f}€)")

t_stop = perf_counter()
print(f"\nTime taken: {t_stop - t_start:.4f} seconds")
