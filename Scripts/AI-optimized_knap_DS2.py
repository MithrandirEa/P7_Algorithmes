"""
Je ne comprends pas encore la logique du KnapSack. Ce script est générer par l'ia afin de pouvoir comparer avec mes scripts.
"""

import pandas as pd
from time import perf_counter

t_start = perf_counter()


def knapsack_01(actions, max_budget):
    """Algorithme du sac à dos 0/1 par programmation dynamique optimisée"""
    n = len(actions)
    budget_cents = int(max_budget * 100)
    
    prices = [int(action['price'] * 100) for action in actions]
    benefits = [action['benefit_2y'] for action in actions]
    
    # Table DP optimisée: seulement 2 lignes au lieu de n+1
    prev = [0.0] * (budget_cents + 1)
    curr = [0.0] * (budget_cents + 1)
    
    # Matrice pour le backtracking
    keep = [[False] * (budget_cents + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        price = prices[i - 1]
        benefit = benefits[i - 1]
        
        for w in range(budget_cents + 1):
            if price > w:
                curr[w] = prev[w]
            else:
                without = prev[w]
                with_item = prev[w - price] + benefit
                if with_item > without:
                    curr[w] = with_item
                    keep[i][w] = True
                else:
                    curr[w] = without
        
        prev, curr = curr, prev
    
    # Backtracking
    selected = []
    w = budget_cents
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected.append(actions[i - 1])
            w -= prices[i - 1]
    
    selected.reverse()
    return prev[budget_cents], selected


df = pd.read_csv("first_search/data/dataset_2.csv")
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
