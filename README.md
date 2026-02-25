# 📈 P7_Algorithmes — Optimisation de Portefeuille d'Actions

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

Projet OpenClassroom C7. Objectif: composer un portefeuille maximisant le bénéfice sur 2 ans sous contraintes de budget (500€), d'unicité (chaque action au plus une fois) et d'insécabilité.

## 🎯 Objectifs
- **Maximiser** le bénéfice total sur 2 ans.
- **Respecter** un budget total ≤ 500€.
- **Contrainte** : Une action ne peut être achetée qu'une seule fois et n'est pas fractionnable (problème du sac à dos 0/1).

## 📊 Datasets
- `data/Actions.csv` (20 actions) — prototypage rapide / démo algorithme force brute.
- `data/dataset_1.csv` (1000 actions) — production.
- `data/dataset_2.csv` (1000 actions) — production.

**Note sur les données :**
Les colonnes utilisées sont `name`, `price` (en €), et `profit` (en %).
Le bénéfice absolu est calculé comme : `price * profit / 100`.

## 🚀 Algorithmes

### 1) Brute Force (recherche exhaustive)
- Complexité temps: O(2^n). Complexité mémoire: O(n).
- Garantit l'optimalité mais impraticable pour de grands n (timeout appliqué).
- Script principal: `bruteforce.py`.

### 2) Programmation Dynamique
- Modélisation knapsack 0/1 avec conversion des prix en centimes.
- Complexité temps: O(n × W) avec W = budget en centimes. Mémoire: O(W).
- Scripts: `Scripts/alpha_opti.py`, `Scripts/DS1_opti.py`, `Scripts/DS2_opti.py`.

### 3) DP optimisée Numba (JIT)
- Même logique DP, compilée avec Numba pour accélérer les boucles critiques.
- Complexité temps: O(n × W) (plus rapide en pratique). Mémoire: O(W).
- Scripts: `Scripts/DS1_opti2.py`, `Scripts/DS2_opti2.py`.
- Remarque: Numba est inclus via `requirements.txt`.

## 🗃️ Vue d'ensemble des scripts
| Script              | Dataset         | Algorithme            | Notes |
|---------------------|-----------------|-----------------------|-------|
| `bruteforce.py`     | Interactif      | Brute Force           | Timeout de sécurité |
| `alpha_opti.py`     | Actions.csv     | Knapsack DP           | Démo 20 actions |
| `DS1_opti.py`       | dataset_1.csv   | Knapsack DP           | Optimal |
| `DS1_opti2.py`      | dataset_1.csv   | Knapsack DP + Numba   | JIT accéléré |
| `DS2_opti.py`       | dataset_2.csv   | Knapsack DP           | Optimal |
| `DS2_opti2.py`      | dataset_2.csv   | Knapsack DP + Numba   | JIT accéléré |

## 🧰 Installation
Prérequis: Python 3.10+, pip

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

## ▶️ Utilisation rapide

### Brute Force (interactif)
```powershell
python bruteforce.py
# Entrez le chemin du dataset (ex: data/dataset_1.csv)
```

### Scripts optimisés
```powershell
python Scripts/alpha_opti.py
python Scripts/DS1_opti.py
python Scripts/DS1_opti2.py
```

### Outil de benchmark
```powershell
# Un script spécifique
python speed_test.py Scripts/DS1_opti2.py
# Tous les scripts du dossier Scripts
python speed_test.py --all
```

L'outil affiche un récapitulatif (temps total, temps interne si disponible, statut, prix total, bénéfice total) et détecte automatiquement le dataset en lisant le script.

## 🧮 Complexité (résumé)
| Algorithme         | Temps     | Espace | Optimal |
|--------------------|----------|--------|---------|
| Brute Force        | O(2^n)   | O(n)   | ✅ |
| DP 			     | O(n×W)   | O(W)   | ✅ |
| DP (Numba JIT)     | O(n×W)   | O(W)   | ✅ |

n = nombre d'actions, W = budget en centimes.

## 📁 Structure du projet
```
P7_Algorithmes/
├── Scripts/
│   ├── alpha_opti.py
│   ├── DS1_opti.py
│   ├── DS1_opti2.py
│   ├── DS2_opti.py
│   └── DS2_opti2.py
├── data/
│   ├── Actions.csv
│   ├── dataset_1.csv
│   ├── dataset_2.csv
│   ├── Decisions_achat_1.txt
│   └── Decisions-achat-2.txt
├── bruteforce.py
├── speed_test.py
├── requirements.txt
└── README.md
```

## 🔧 Notes
- Les scripts DP utilisent une table 1D (`O(W)`) et une matrice `keep` pour reconstituer la solution.
- Les versions Numba requièrent que les tableaux passés à la fonction JIT soient des `numpy.ndarray` typés (fait dans les scripts `*_opti2`).
- Dans `bruteforce.py`, la colonne CSV `profit` est directement mappée à `benefit_2y` (même unité: euros).

## 📝 Licence & Auteur
Projet éducatif OpenClassroom — C7 - Par SCIPION Clément

Auteur: **MithrandirEa**
- GitHub: https://github.com/MithrandirEa
- Repo: https://github.com/MithrandirEa/P7_Algorithmes

Dernière mise à jour: 18 décembre 2025
