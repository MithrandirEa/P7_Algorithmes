import csv
from itertools import combinations
from time import perf_counter

t_start = perf_counter()

def read_actions_from_csv(file):
    """Lit les actions depuis un fichier CSV avec gestion des pourcentages"""
    actions = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            coast = float(row['price'])
            benefit = float(row['benefit_2y'])
            actions.append({
                'name': row['name'],
                'price': coast,
                'benefit_2y': benefit
            })
    return actions


def find_best_combination(actions, max_budget=500):
    """Trouve la meilleure combinaison d'actions respectant le budget
    maximum"""
    best_combination = None
    max_benefit = 0
    n = len(actions)
    
    # Générer et évaluer toutes les combinaisons possibles
    for r in range(n + 1):
        for combo in combinations(actions, r):
            total_coast = sum(action['price'] for action in combo)
            
            # Vérifier si la combinaison respecte le budget
            if total_coast <= max_budget:
                total_benefit = sum(action['benefit_2y'] for action in combo)
                
                # Mettre à jour si c'est la meilleure combinaison
                if total_benefit > max_benefit:
                    max_benefit = total_benefit
                    best_combination = {
                        'actions': combo,
                        'total_coast': total_coast,
                        'total_benefit': total_benefit
                    }
    
    return best_combination


# Lecture des actions et recherche de la meilleure combinaison
actions = read_actions_from_csv('first_search/data/dataset_1_cured.csv')
best = find_best_combination(actions)
# Affichage du résultat
if best:
    print("Best combination:")
    print(f"Total price: {best['total_coast']:.2f} euros")
    print(f"Total benefit: {best['total_benefit']:.2f} euros")
    print("Selected actions:")
    for action in best['actions']:
        print(f"  - {action['name']}: {action['coast']:.2f}€ "
              f"(benefit: {action['benefit']:.2f}€)")

t_stop = perf_counter()
print(f"\nTime taken: {t_stop - t_start:.4f} seconds")