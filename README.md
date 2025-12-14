
# 📈 P7_Algorithmes - Optimisation de Portefeuille d'Actions

Projet OpenClassroom C7 : Résoudre des problèmes d'optimisation de portefeuille d'actions en Python

## 🎯 Objectif

Développer et comparer plusieurs algorithmes pour maximiser le profit sur 2 ans, sous contraintes :
- Une action ne peut être achetée qu'une seule fois
- Une action est insécable
- Budget maximum : **500€**

## 📊 Datasets

- `Actions.csv` : 20 actions (prototypage)
- `dataset_1.csv` & `dataset_2.csv` : 1000 actions (production)
	- Nettoyage : suppression NaN, prix/profit négatifs, calcul `benefit_2y = price × profit / 100`

## 🚀 Algorithmes Implémentés

### 1️⃣ Brute Force (Recherche exhaustive)
- **Scripts :** `alpha_BF.py`, `DS1_BF.py`, `DS2_BF.py`
- **Complexité :** O(2ⁿ)
- **Usage :**
	```bash
	python Scripts/alpha_BF.py
	python Scripts/DS1_BF.py
	python Scripts/DS2_BF.py
	```
- **Remarque :** Timeout 10s pour les gros datasets

### 2️⃣ Knapsack (Programmation Dynamique)
- **Scripts :** `alpha_opti.py`, `DS1_opti.py`, `DS2_opti.py`
- **Complexité :** O(n × W) (W = budget en centimes)
- **Usage :**
	```bash
	python Scripts/alpha_opti.py
	python Scripts/DS1_opti.py
	python Scripts/DS2_opti.py
	```
- **Remarque :** Solution optimale, rapide pour n ≤ 1000

### 3️⃣ Knapsack optimisé Numba (JIT)
- **Scripts :** `DS1_opti2.py.py`, `DS2_opti2.py`
- **Complexité :** O(n × W) mais accéléré par Numba
- **Usage :**
	```bash
	python Scripts/DS1_opti2.py.py
	python Scripts/DS2_opti2.py
	```
- **Remarque :** Identique à la version DP mais 5-10x plus rapide grâce à la compilation JIT

### 4️⃣ Résumé des scripts

| Script              | Dataset         | Algorithme         | Optimisation |
|---------------------|----------------|--------------------|--------------|
| alpha_BF.py         | Actions.csv    | Brute Force        | -            |
| alpha_opti.py       | Actions.csv    | Knapsack DP        | -            |
| DS1_BF.py           | dataset_1.csv  | Brute Force        | -            |
| DS1_opti.py         | dataset_1.csv  | Knapsack DP        | -            |
| DS1_opti2.py.py     | dataset_1.csv  | Knapsack DP        | Numba        |
| DS2_BF.py           | dataset_2.csv  | Brute Force        | -            |
| DS2_opti.py         | dataset_2.csv  | Knapsack DP        | -            |
| DS2_opti2.py        | dataset_2.csv  | Knapsack DP        | Numba        |

## 🛠️ Outil de Benchmark

### speed_test.py
Script de mesure de performance d'exécution avec enregistrement automatique des résultats.

**Fonctionnalités :**
- Mesure du temps d'exécution réel et interne
- Extraction automatique du prix total et bénéfice total
- Détection automatique du dataset utilisé
- Logs CSV avec horodatage
- Tableau récapitulatif

**Usage :**
```bash
# Tester un script spécifique
python speed_test.py Scripts/DS1_opti2.py.py
# Tester tous les scripts du dossier Scripts
python speed_test.py --all
```

## 📦 Installation

### Prérequis
- Python 3.10+
- pip


### Dépendances

```bash
# Créer un environnement virtuel
python -m venv .venv
# Activer l'environnement (Windows)
.venv\Scripts\activate
# Installer toutes les dépendances (y compris Numba)
pip install -r requirements.txt
```

> **Remarque :** Numba est requis pour exécuter les scripts _opti2. Il est maintenant inclus dans requirements.txt.

## 🏃 Démarrage Rapide

```bash
# 1. Tester l'algorithme optimisé Numba sur dataset 1
python Scripts/DS1_opti2.py.py
# 2. Comparer avec la version DP classique
python Scripts/DS1_opti.py
# 3. Benchmarker tous les scripts
python speed_test.py --all
```

## 🧮 Complexité Algorithmique

| Algorithme         | Temps         | Espace      | Optimal  |
|--------------------|---------------|-------------|----------|
| Brute Force        | O(2ⁿ)         | O(n)        | ✅      |
| DP                 | O(n × W)      | O(W)        | ✅      |
| Numba              | O(n × W)      | O(W)        | ✅      |

## 📋 Structure du Projet


```
P7_Algorithmes/
│
├── Scripts/
│   ├── alpha_BF.py
│   ├── alpha_opti.py
│   ├── DS1_BF.py
│   ├── DS1_opti.py
│   ├── DS1_opti2.py.py
│   ├── DS2_BF.py
│   ├── DS2_opti.py
│   ├── DS2_opti2.py
│   └── ...
├── data/
│   ├── Actions.csv
│   ├── dataset_1.csv
│   ├── dataset_2.csv
│   └── Decisions_achat_*.txt
├── speed_test.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Non suivis par git (ignorés) :**
- `.venv/` (environnement virtuel Python)
- `.vscode/` (config VS Code)
- `data/speed_test_records.csv` (logs de benchmark)
- `first_search/` (dossier de travail temporaire)
- `*.ipynb` (notebooks Jupyter)
- `Numba_test.md` (notes/tests temporaires)

## 🔧 Améliorations Possibles

1. **Branch & Bound** : Accélérer le brute-force avec élagage
2. **FPTAS** : Approximation rapide du knapsack
3. **API REST** : Exposer les algos via une API web
4. **Interface graphique** : Visualisation interactive

## 📄 Licence

Projet éducatif OpenClassroom - C7

## 👤 Auteur

**MithrandirEa**
- GitHub: [@MithrandirEa](https://github.com/MithrandirEa)
- Repository: [P7_Algorithmes](https://github.com/MithrandirEa/P7_Algorithmes)

---

*Dernière mise à jour : 15 décembre 2025*

## 🛠️ Outil de Benchmark

### speed_test.py

Script de mesure de performance d'exécution avec enregistrement automatique des résultats.

**Fonctionnalités :**
- Mesure du temps d'exécution réel (subprocess) et interne (script)
- Extraction automatique du prix total et bénéfice total
- Détection automatique du dataset utilisé
- Gestion des timeouts et erreurs
- Logs CSV avec horodatage
- Tableau récapitulatif avec 7 colonnes : Script, Dataset, Temps, T.Script, Status, Prix, Bénéfice

**Usage :**

```bash
# Tester un script spécifique
python speed_test.py Scripts/brute_force_alpha.py

# Tester tous les scripts du dossier Scripts
python speed_test.py --all

# Afficher l'aide
python speed_test.py --help
```

**Logs :** Les résultats sont enregistrés dans `data/speed_test_records.csv` avec les colonnes :
- `timestamp` : Date et heure d'exécution
- `script_name` : Nom du script
- `script_path` : Chemin complet
- `dataset_used` : Dataset détecté
- `execution_time_seconds` : Temps d'exécution
- `status` : success | error | timeout
- `error_message` : Message d'erreur simplifié (ex: "Timeout")

## 📦 Installation

### Prérequis
- Python 3.10+
- pip

### Dépendances

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🏃 Démarrage Rapide

```bash
# 1. Tester l'algorithme optimisé sur dataset 1
python Scripts/optimized_DS1.py

# 2. Comparer avec le brute-force (attention au timeout=10s)
python Scripts/brute_force_alpha.py

# 3. Benchmarker tous les scripts
python speed_test.py --all
```

## 🧮 Complexité Algorithmique

### Brute Force
- **Temps :** O(2ⁿ) où n = nombre d'actions
- **Espace :** O(n)
- **Optimal :** ✅ Oui (si termine)

### Optimized (Greedy)
- **Temps :** O(n log n) (dominé par le tri)
- **Espace :** O(n)
- **Optimal :** ⚠️ Quasi-optimal (heuristique gloutonne)

### Knapsack (Programmation Dynamique)
- **Temps :** O(n × W) où W = budget × 100 (en centimes)
- **Espace :** O(W) (optimisé avec 2 lignes au lieu de n×W)
- **Optimal :** ✅ Oui (solution garantie optimale)

## 📊 Bilan Big O par fichier

| Fichier                   | Algorithme      | Complexité Temps | Complexité Mémoire |
|---------------------------|-----------------|------------------|--------------------|
| DS1_clean.py, DS2_clean.py| Greedy          | O(n log n)       | O(n)               |
| DS1_opti.py, DS2_opti.py  | Knapsack DP     | O(n × W)         | O(n × W) / O(W)    |
| AI-optimized_knap_DS1.py, AI-optimized_knap_DS2.py, optimized_DS1.py, optimized_DS2.py, alpha_opti.py | Knapsack DP | O(n × W) | O(n × W) / O(W) |
| DS1_BF.py, DS2_BF.py, alpha_BF.py | Brute Force | O(2ⁿ) | O(n) |

- **n** = nombre d'actions, **W** = budget (en centimes)
- Les scripts Knapsack DP utilisent numpy et une table DP 1D pour accélérer le calcul.

## 📋 Répartition des scripts par algorithme

- **Greedy** : DS1_clean.py, DS2_clean.py, DS1_opti.py, DS2_opti.py
- **DP** : AI-optimized_knap_DS1.py, AI-optimized_knap_DS2.py, optimized_DS1.py, optimized_DS2.py, alpha_opti.py
- **Brute Force** : DS1_BF.py, DS2_BF.py, alpha_BF.py


## 🕒 Date de dernière mise à jour

*Dernière mise à jour : 4 décembre 2025*

## 📝 Structure du Projet

```
P7_Algorithmes/
│
├── Scripts/
│   ├── brute_force_alpha.py       # Brute force sur Actions.csv
│   ├── brute_force_DS1.py         # Brute force dataset 1 (timeout 10s)
│   ├── brute_force_DS2.py         # Brute force dataset 2 (timeout 10s)
│   ├── optimized_DS1.py           # Algorithme Greedy dataset 1
│   ├── optimized_DS2.py           # Algorithme Greedy dataset 2
│   ├── AI-optimized_knap_DS1.py   # Knapsack DP dataset 1
│   └── AI-optimized_knap_DS2.py   # Knapsack DP dataset 2
│
├── data/
│   ├── Actions.csv                # Dataset initial (20 actions)
│   ├── dataset_1.csv              # Dataset 1 (1000 actions)
│   ├── dataset_2.csv              # Dataset 2 (1000 actions)
│   ├── speed_test_records.csv     # Logs de performance
│   └── Decisions_achat_*.txt      # Décisions d'achat exportées
│
├── speed_test.py                  # Outil de benchmark
├── requirements.txt               # Dépendances Python
├── .gitignore
└── README.md                      # Ce fichier

```

## 📄 Licence

Projet éducatif OpenClassroom - C7

## 👤 Auteur

**MithrandirEa**
- GitHub: [@MithrandirEa](https://github.com/MithrandirEa)
- Repository: [P7_Algorithmes](https://github.com/MithrandirEa/P7_Algorithmes)

---

*Dernière mise à jour : 4 décembre 2025*
