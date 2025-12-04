import csv
from itertools import combinations
from time import perf_counter

t_start = perf_counter()
TIMEOUT_SECONDS = 10  # 10 seconds


def read_actions_from_csv(file="first_search/data/dataset_2.csv"):
    """Lit les actions depuis un fichier CSV avec gestion des pourcentages"""
    actions = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            coast = float(row["price"])
            benefit = float(row["benefit_2y"])
            actions.append({"name": row["name"], "price": coast, "benefit_2y": benefit})
    return actions


def find_best_combination(actions, max_budget=500, timeout=TIMEOUT_SECONDS):
    """Trouve la meilleure combinaison d'actions respectant le budget
    maximum avec un timeout"""
    best_combination = None
    max_benefit = 0
    n = len(actions)
    start_time = perf_counter()

    # Générer et évaluer toutes les combinaisons possibles
    for r in range(n + 1):
        for combo in combinations(actions, r):
            # Vérifier le timeout
            if perf_counter() - start_time > timeout:
                raise TimeoutError("Timeout reached")
            
            total_coast = sum(action["price"] for action in combo)

            # Vérifier si la combinaison respecte le budget
            if total_coast <= max_budget:
                total_benefit = sum(action["benefit_2y"] for action in combo)

                # Mettre à jour si c'est la meilleure combinaison
                if total_benefit > max_benefit:
                    max_benefit = total_benefit
                    best_combination = {
                        "actions": combo,
                        "total_coast": total_coast,
                        "total_benefit": total_benefit,
                    }

    return best_combination


# Lecture des actions et recherche de la meilleure combinaison
actions = read_actions_from_csv("data/dataset_2.csv")
best = find_best_combination(actions)

# Affichage du résultat
t_stop = perf_counter()
elapsed_time = t_stop - t_start

if best:
    print("Best combination:")
    print(f"Total price: {best['total_coast']:.2f} euros")
    print(f"Total benefit: {best['total_benefit']:.2f} euros")
    print(f"Number of actions: {len(best['actions'])}")
    print("Selected actions:")
    for action in best["actions"]:
        print(
            f"  - {action['name']}: {action['price']:.2f}€ "
            f"(benefit: {action['benefit_2y']:.2f}€)"
        )
else:
    print("⚠️ Aucune combinaison trouvée dans le temps imparti")

print(f"\n⏱️ Time taken: {elapsed_time:.4f} seconds")

