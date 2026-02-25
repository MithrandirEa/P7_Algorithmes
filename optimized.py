"""
Script d'optimisation (Sac à dos) utilisant la programmation dynamique.

Ce script résout le problème du sac à dos 0/1 pour optimiser un portefeuille
d'actions. Il utilise une approche de programmation dynamique compilée à
la volée (JIT) avec Numba pour des performances maximales.
Complexité temporelle : O(n * W) où n est le nombre d'actions et W la capacité
(budgétaire) du sac à dos.
"""

from time import perf_counter
import pandas as pd
import numpy as np
from numba import njit


"""
Le décorateur @njit compile la fonction knapsack_numba en code machine
optimisé. Cela permet une exécution beaucoup plus rapide des boucles imbriquées
typiques de la programmation dynamique, rivalisant avec C/C++.
"""


@njit
def knapsack_numba(prices, benefits, n, max_budget_cents):
    """
    Algorithme du sac à dos (Knapsack) optimisé avec Numba.

    Args:
        prices (numpy.ndarray): Tableau des prix des actions (entiers).
        benefits (numpy.ndarray): Tableau des bénéfices (flottants).
        n (int): Nombre d'actions.
        max_budget_cents (int): Budget max en centimes (évite erreurs float).

    Returns:
        tuple: (dp, keep)
            - dp (array): Bénéfice max pour chaque budget w.
            - keep (array): Tableau booléen pour reconstruire la solution.
    """
    # dp[w] stockera le profit maximum pour une capacité w
    dp = np.zeros(max_budget_cents + 1, dtype=np.float32)

    # keep[i, w] stocke si l'objet i a été pris pour la capacité w
    keep = np.zeros((n, max_budget_cents + 1), dtype=np.bool_)

    for i in range(n):
        price = prices[i]
        benefit = benefits[i]
        # On parcourt le budget de max vers min pour simuler un tableau 2D
        for w in range(max_budget_cents, price - 1, -1):
            if dp[w - price] + benefit > dp[w]:
                dp[w] = dp[w - price] + benefit
                keep[i, w] = True
    return dp, keep


def main():
    """Fonction principale gérant le chargement des données et l'exécution."""
    # Chargement et nettoyage des données avec Pandas
    try:
        path = input("Entrez le chemin du dataset (ex: data/dataset_1.csv) : ")
        if not path:
            dataset_path = "data/dataset_1.csv"
            print(f"Utilisation du fichier par défaut : {dataset_path}")
        else:
            dataset_path = path

        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return

    # Prétraitement : suppression des valeurs manquantes et incohérentes
    df = df.dropna()
    df = df[(df['price'] > 0) & (df['profit'] >= 0)]
    df = df.reset_index(drop=True)

    # Calcul du bénéfice absolu avant le traitement
    df['benefit_2y'] = df['price'] * df['profit'] / 100

    # Conversion en tableaux NumPy pour Numba
    # Les prix sont convertis en centimes (entiers) pour éviter erreurs float
    prices = (df['price'] * 100).round().astype(np.int32).to_numpy()
    benefits = df['benefit_2y'].to_numpy(dtype=np.float32)
    n = len(prices)
    max_budget = 500
    max_budget_cents = max_budget * 100

    print("Démarrage du calcul...")
    t_start = perf_counter()

    # Appel de la fonction compilée JIT
    dp, keep = knapsack_numba(prices, benefits, n, max_budget_cents)

    # Backtracking pour retrouver les actions sélectionnées
    # On reconstruit la solution optimale en remontant le tableau 'keep'
    w_idx = np.argmax(dp)
    selected_indices = []

    # Parcours inverse pour identifier les éléments choisis
    for i in range(n - 1, -1, -1):
        if w_idx >= prices[i] and keep[i, w_idx]:
            selected_indices.append(i)
            w_idx -= prices[i]

    # On remet dans l'ordre (optionnel mais plus propre)
    selected_indices.reverse()

    # Extraction des résultats finaux via Pandas
    selected_actions = df.iloc[selected_indices]
    t_stop = perf_counter()

    # Affichage des résultats détaillée
    print("\n--- Résultat Optimisé ---")
    for _, action in selected_actions.iterrows():
        print(f"  - {action['name']}: Prix={action['price']:.2f}€, "
              f"Bénéfice={action['benefit_2y']:.2f}€")

    total_price = selected_actions['price'].sum()
    total_benefit = selected_actions['benefit_2y'].sum()

    print("\nRésumé :")
    print(f"  Prix total investissement : {total_price:.2f} euros")
    print(f"  Profit total sur 2 ans    : {total_benefit:.2f} euros")
    print(f"  Nombre d'actions retenues : {len(selected_actions)}")
    print(f"  Temps d'exécution         : {t_stop - t_start:.4f} secondes")


if __name__ == "__main__":
    main()
