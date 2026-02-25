"""
Script de force brute pour le problème du sac à dos (Knapsack Problem).

Ce script explore toutes les combinaisons possibles d'actions pour trouver
celle qui maximise le profit tout en respectant un budget donné.
La complexité temporelle est de O(2^n), ce qui le rend inutilisable pour
un grand nombre d'actions (n > 20-25).
"""

import csv
from itertools import combinations
from time import perf_counter

# Configuration par défaut
TIMEOUT_SECONDS = 10  # Timeout de 10s pour la demo


def read_actions_from_csv(file):
    """
    Lit les actions depuis un fichier CSV et calcule le bénéfice réel.

    Args:
        file (str): Chemin vers le fichier CSV contenant les actions.
                    Le fichier doit avoir les colonnes 'name', 'price',
                    'profit'.

    Returns:
        list: Une liste de dictionnaires représentant les actions validées.
              Chaque action a les clés 'name', 'price', 'benefit_2y'.
    """
    actions = []
    with open(file, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Gestion des noms de colonnes variables (dataset vs Actions)
                name = row.get("name") or row.get("Actions")
                price_str = row.get("price") or row.get("Coast")
                profit_str = row.get("profit") or row.get("Benefit")

                if not (name and price_str and profit_str):
                    continue

                # Nettoyage et conversion
                price = float(price_str.replace('€', '').strip())
                profit_percentage = float(profit_str.replace('%', '').strip())

                # On ne garde que les actions avec un prix strictement positif
                if price > 0:
                    actions.append({
                        "name": name,
                        "price": price,
                        "benefit_2y": price * profit_percentage / 100
                    })
            except ValueError:
                continue

    return actions


def find_best_combination(actions, max_budget=500, timeout=TIMEOUT_SECONDS):
    """
    Trouve la meilleure combinaison d'actions respectant le budget.

    Cette fonction génère toutes les combinaisons possibles (de taille 1 à n)
    et évalue leur coût et leur bénéfice.

    Args:
        actions (list): Liste de dictionnaires d'actions.
        max_budget (float): Budget maximum d'investissement.
        timeout (int): Temps maximum d'exécution en secondes.

    Returns:
        dict: La meilleure combinaison trouvée avec 'actions', 'total_coast',
              et 'total_benefit'. Retourne None si aucune combinaison valide.

    Raises:
        TimeoutError: Si l'exécution dépasse le temps imparti.
    """
    best_combination = None
    max_benefit = 0
    n = len(actions)
    start_time = perf_counter()

    # Générer et évaluer toutes les combinaisons possibles
    # La boucle externe détermine la taille de la combinaison (r actions)
    for r in range(n + 1):
        for combo in combinations(actions, r):
            # Vérifier le timeout à chaque itération pour éviter de bloquer
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


if __name__ == "__main__":
    t_start = perf_counter()

    # Demande interactive du fichier si exécuté en tant que script principal
    try:
        path = input("Entrez le chemin du dataset (ex: data/Actions.csv) : ")
        if not path:
            DATASET_PATH = "data/Actions.csv"  # Valeur par défaut
            print(f"Utilisation du fichier par défaut: {DATASET_PATH}")
        else:
            DATASET_PATH = path

        actions = read_actions_from_csv(DATASET_PATH)

        print(f"Analyse de {len(actions)} actions...")
        best = find_best_combination(actions)

        # Affichage du résultat
        t_stop = perf_counter()
        elapsed_time = t_stop - t_start

        if best:
            print("\n✅ Meilleure combinaison trouvée :")
            print(f"  Coût total : {best['total_coast']:.2f} euros")
            print(f"  Bénéfice total : {best['total_benefit']:.2f} euros")
            print(f"  Nombre d'actions : {len(best['actions'])}")
            print("\nListe des actions retenues :")
            for action in best["actions"]:
                print(
                    f"  - {action['name']} : {action['price']:.2f}€ "
                    f"(Bénéfice : {action['benefit_2y']:.2f}€)"
                )
        else:
            print("⚠️ Aucune combinaison trouvée ou budget trop faible.")

        print(f"\n⏱️ Temps d'exécution : {elapsed_time:.4f} secondes")

    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{DATASET_PATH}' est introuvable.")
    except TimeoutError:
        print("❌ Erreur : Le traitement a pris trop de temps (Timeout).")
    except Exception as e:
        print(f"❌ Une erreur s'est produite : {e}")
