# 📈 P7_Algorithmes - Optimisation de Portefeuille d'Actions

Projet OpenClassroom C7 : Résoudre des problèmes en utilisant des algorithmes en Python

## 🎯 Objectif

Développer des algorithmes pour composer un portefeuille d'actions maximisant le profit sur 2 ans, sous trois contraintes :
- ✅ Une action ne peut être achetée qu'une seule fois
- ✅ Une action est insécable (pas de fractionnement)
- ✅ Budget maximum : **500€**

## 📊 Datasets

### Actions.csv (20 actions)
Dataset initial pour les tests rapides et le prototypage.

### dataset_1.csv & dataset_2.csv (1000 actions)
Datasets de production après nettoyage :
- Suppression des valeurs NaN
- Filtrage des prix et profits négatifs ou nuls
- Calcul du bénéfice sur 2 ans : `benefit_2y = price × profit / 100`

## 🚀 Algorithmes Implémentés

### 1️⃣ Brute Force (Recherche Exhaustive)

**Complexité :** O(2ⁿ) - Exponentielle

**Principe :** Génère et évalue toutes les combinaisons possibles d'actions.

**Fichiers :**
- `Scripts/brute_force_alpha.py` - Version de base sur Actions.csv
- `Scripts/brute_force_DS1.py` - Dataset 1 avec timeout 10s
- `Scripts/brute_force_DS2.py` - Dataset 2 avec timeout 10s

**Caractéristiques :**
- ✅ Garantit la solution optimale
- ⚠️ Timeout de 10 secondes pour éviter les temps d'exécution trop longs
- ❌ Non viable pour datasets de grande taille (>25 actions)

```python
# Exemple d'utilisation
python Scripts/brute_force_alpha.py
```

### 2️⃣ Algorithme Optimisé (Greedy)

**Complexité :** O(n log n) - Linéarithmique

**Principe :** Algorithme glouton qui trie les actions par pourcentage de profit décroissant, puis sélectionne les actions tant que le budget le permet.

**Fichiers :**
- `Scripts/optimized_DS1.py` - Version optimisée pour dataset 1
- `Scripts/optimized_DS2.py` - Version optimisée pour dataset 2

**Performances :**
- 🎯 Utilisation du budget : ~100% (499.94-499.98€)
- 📈 Rendement global : ~39.5-39.7%
- ⚡ Temps d'exécution : ~0.02 secondes

**Avantages :**
- ✅ Très rapide (même sur 1000+ actions)
- ✅ Excellente utilisation du budget
- ✅ Solution quasi-optimale

```python
# Exemple d'utilisation
python Scripts/optimized_DS1.py
```

### 3️⃣ Algorithme Knapsack (Programmation Dynamique)

**Complexité :** O(n × W) où W = capacité du sac (budget)

**Principe :** Utilise la programmation dynamique pour garantir la solution optimale. L'algorithme construit une table DP en convertissant les prix en centimes pour éviter les décimales.

**Fichiers :**
- `Scripts/AI-optimized_knap_DS1.py` - Knapsack optimisé pour dataset 1
- `Scripts/AI-optimized_knap_DS2.py` - Knapsack optimisé pour dataset 2

**Performances :**
- 🎯 Utilisation du budget : ~99.99% (499.92-499.96€)
- 📈 Rendement global : ~39.6-39.7%
- ⚡ Temps d'exécution : ~1.5-3.0 secondes (interne), ~1.9-3.0s (total)

**Avantages :**
- ✅ Solution garantie optimale (contrairement au greedy)
- ✅ Temps raisonnable même sur 1000 actions
- ✅ Optimisation mémoire (2 lignes au lieu de n×W)

```python
# Exemple d'utilisation
python Scripts/AI-optimized_knap_DS1.py
```

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
- **Knapsack DP** : AI-optimized_knap_DS1.py, AI-optimized_knap_DS2.py, optimized_DS1.py, optimized_DS2.py, alpha_opti.py
- **Brute Force** : DS1_BF.py, DS2_BF.py, alpha_BF.py

## ⚡ Note sur l'optimisation FPTAS

Pour passer sous la barre de 1 seconde sur 1000 actions, il est possible d'utiliser une version FPTAS du knapsack :
- On réduit la granularité du budget (ex : arrondi à 0.5€ ou 1€)
- La complexité devient O(n × W') avec W' << W
- La solution reste quasi-optimale (écart <0.1%)

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

## 🎓 Concepts Clés

### Problème du Sac à Dos (Knapsack Problem)
Ce projet est une variante du problème classique du sac à dos 0/1 :
- Chaque action a un **poids** (prix) et une **valeur** (bénéfice)
- On cherche à maximiser la valeur totale sans dépasser la capacité (500€)

### Algorithme Glouton (Greedy)
L'algorithme optimisé utilise une stratégie gloutonne :
1. Calculer le ratio profit/prix pour chaque action
2. Trier par profit décroissant (déjà le ratio dans notre cas)
3. Sélectionner les actions dans l'ordre tant que le budget le permet

**Pourquoi ça marche ?**
Le tri par pourcentage de profit maximise le rendement par euro investi, assurant une utilisation optimale du budget.

## 🔧 Améliorations Possibles

1. **Branch & Bound** : Accélérer le brute-force avec élagage intelligent
2. **Algorithmes avancés** : Branch & Cut, FPTAS (Fully Polynomial Time Approximation Scheme)
3. **Génération de rapports PDF** : Export automatique des résultats avec graphiques
4. **API REST** : Exposer les algorithmes via une API web
5. **Interface graphique** : Visualisation interactive des résultats et comparaisons
6. **Analyse de sensibilité** : Impact de la variation du budget sur les résultats

## 📄 Licence

Projet éducatif OpenClassroom - C7

## 👤 Auteur

**MithrandirEa**
- GitHub: [@MithrandirEa](https://github.com/MithrandirEa)
- Repository: [P7_Algorithmes](https://github.com/MithrandirEa/P7_Algorithmes)

---

*Dernière mise à jour : 4 décembre 2025*
