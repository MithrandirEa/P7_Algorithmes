import pandas as pd
from time import perf_counter

t_start = perf_counter()

df = pd.read_csv("first_search/data/dataset_1.csv")

""" Supprime toutes les lignes avec des valeurs nulles en prix et profit car ça n'aurait pas de sens de calculer"""
df = df.dropna(subset=["price", "profit"])
df = df[(df["price"] > 0) & (df["profit"] > 0)]

df["benefit_2y"] = df["price"] * df["profit"] / 100

# Trier par profit (pourcentage de rendement) décroissant
df = df.sort_values("profit", ascending=False)


total_price = 0
total_benefit = 0
selected_actions = []

for index, row in df.iterrows():
    if total_price + row["price"] <= 500:
        total_price += row["price"]
        total_benefit += row["benefit_2y"]
        selected_actions.append(
            {"name": row["name"], "price": row["price"], "benefit": row["benefit_2y"]}
        )

budget_utilise_pct = (total_price / 500) * 100
rendement_global = (total_benefit / total_price * 100) if total_price > 0 else 0

print(f"Prix total du bouquet d'actions: {total_price:.2f} euros")
print(f"Budget utilisé: {budget_utilise_pct:.2f}%")
print(f"Profit total des actions sélectionnées sur 2 ans: {total_benefit:.2f} euros")
print(f"Rendement global: {rendement_global:.2f}%")
print(f"Nombre d'actions: {len(selected_actions)}")
print("\nActions sélectionnées (triées par rendement):")
for action in selected_actions:
    print(
        f" - {action['name']:20s} - {action['price']:8.2f}€ (bénéfice : {action['benefit']:8.2f}€)"
    )

t_stop = perf_counter()
print(f"\nTime taken: {t_stop - t_start:.4f} seconds")
