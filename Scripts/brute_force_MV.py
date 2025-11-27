"""
Brute-force.py est un script python qui cherche à composer par brute-force
un portefeuille d'action maximisant le profit tout en respectant trois
contraintes :
- une action ne peut être achetée qu'une seule fois
- une action est insécable
- le budget total alloué ne peut pas être dépassé. Budget_max = 500 euros

Fonctionnement :
- on génère toutes les combinaisons possibles d'actions
- on filtre les combinaisons respectant la contrainte de budget
- on calcule le prix total et le profit total de chaque combinaison
- on retient la combinaison ayant le profit total le plus élevé

"""

import csv
from itertools import combinations
from time import perf_counter


t_start = perf_counter()

def parse_benefit(coast, benefit_str):
    """Convertit le bénéfice en pourcentage vers une valeur absolue"""
    if isinstance(benefit_str, str) and benefit_str.endswith('%'):
        return coast * float(benefit_str[:-1]) / 100
    return float(benefit_str)


def read_actions_from_csv(file):
    """Lit les actions depuis un fichier CSV avec gestion des pourcentages"""
    actions = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            coast = float(row['Coast'])
            benefit = parse_benefit(coast, row['Benefit'])
            actions.append({
                'name': row['Actions'],
                'coast': coast,
                'benefit': benefit
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
            total_coast = sum(action['coast'] for action in combo)
            
            # Vérifier si la combinaison respecte le budget
            if total_coast <= max_budget:
                total_benefit = sum(action['benefit'] for action in combo)
                
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
actions = read_actions_from_csv('first_search/data/Actions.csv')
best = find_best_combination(actions)
# Affichage du résultat
if best:
    print("Best combination:")
    print(f"Total cost: {best['total_coast']:.2f} euros")
    print(f"Total benefit: {best['total_benefit']:.2f} euros")
    print("Selected actions:")
    for action in best['actions']:
        print(f"  - {action['name']}: {action['coast']:.2f}€ "
              f"(benefit: {action['benefit']:.2f}€)")

t_stop = perf_counter()
print(f"\nTime taken: {t_stop - t_start:.4f} seconds")