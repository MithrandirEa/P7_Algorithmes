"""
Script de test de performance pour les algorithmes d'optimisation.

Ce script exécute successivement différents scripts Python présents dans le
dossier 'Scripts/', mesure leur temps d'exécution, capture leur sortie
standard, et enregistre les résultats dans un fichier CSV
('data/speed_test_records.csv'). Il gère également un timeout.
"""

import csv
import os
import subprocess
import time
import sys
from datetime import datetime
import re  # Simplification de l'import re


def measure_script_execution(
    script_path, log_csv="data/speed_test_records.csv"
):
    """
    Exécute un script Python donné et mesure ses performances.

    Cette fonction lance le script via un sous-processus, capture sa sortie
    (stdout/stderr), extrait des métriques clés (dataset utilisé, prix total,
    bénéfice) et loggue le tout dans un fichier CSV.

    Args:
        script_path (str): Chemin absolu ou relatif vers le script à tester.
        log_csv (str): Chemin vers le fichier CSV de log.

    Returns:
        dict: Un dictionnaire contenant les résultats de l'exécution,
              ou None si le script n'existe pas.
    """

    # Vérifier que le script existe
    if not os.path.exists(script_path):
        print(f"❌ Erreur: Le script '{script_path}' n'existe pas.")
        return None

    # Créer le répertoire data si nécessaire
    os.makedirs(os.path.dirname(log_csv), exist_ok=True)

    # Créer l'en-tête CSV si le fichier n'existe pas
    if not os.path.exists(log_csv):
        with open(log_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp",
                    "script_name",
                    "script_path",
                    "dataset_used",
                    "execution_time_seconds",
                    "status",
                    "error_message",
                ]
            )

    script_name = os.path.basename(script_path)
    timestamp = datetime.now().isoformat()
    error_message = ""
    dataset_used = "unknown"

    # Détecter le dataset utilisé en lisant le code source
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            # Chercher les patterns de datasets
            if "dataset_1" in script_content.lower():
                dataset_used = "dataset_1"
            elif "dataset_2" in script_content.lower():
                dataset_used = "dataset_2"
            elif "actions.csv" in script_content.lower():
                dataset_used = "Actions.csv"
            # Extraction plus précise avec regex
            csv_matches = re.findall(
                r'["\']([^"\']*/)?([^/"\']*(dataset|actions)[^"\']*.csv)["\']',
                script_content,
                re.IGNORECASE
            )
            if csv_matches:
                dataset_used = csv_matches[0][1]  # Prendre le nom du fichier
    except Exception:
        pass

    print(f"\n{'='*60}")
    print(f"🚀 Exécution de: {script_name}")
    print(f"📁 Chemin: {script_path}")
    print(f"📊 Dataset: {dataset_used}")
    print(f"{'='*60}\n")

    try:
        # Mesurer le temps d'exécution
        start_time = time.perf_counter()

        import sys
        python_executable = sys.executable  # Par défaut
        # Si un venv est détecté, utiliser son python
        venv_python = os.path.join('.venv', 'Scripts', 'python.exe')
        if os.path.exists(venv_python):
            python_executable = os.path.abspath(venv_python)
        
        result = subprocess.run(
            [python_executable, script_path],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes timeout
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # Déterminer le status
        if result.returncode == 0:
            status = "success"
            print("✅ Exécution réussie")
        else:
            status = "error"
            # Extraire seulement la dernière ligne du stderr
            if result.stderr:
                error_lines = result.stderr.strip().split('\n')
                last_line = error_lines[-1][:150]
                # Simplifier le message si c'est un timeout
                if "Timeout" in last_line:
                    error_message = "Timeout"
                else:
                    error_message = last_line
            else:
                error_message = f"Exit code {result.returncode}"
            print(f"❌ Erreur: {error_message}")

        # Afficher la sortie
        total_price = None
        total_benefit = None
        script_time = None
        if result.stdout:
            print("\n📤 Sortie standard:")
            print(result.stdout)
            # Extraire prix total, bénéfice total et temps interne depuis stdout
            for line in result.stdout.split('\n'):
                # Recherche des patterns de prix et bénéfice
                # (Pattern matching simplifié pour la lisibilité)
                if any(x in line for x in ['Prix total', 'Total price']):
                    match = re.search(r'([\d.]+)\s*euros?', line)
                    if match:
                        total_price = float(match.group(1))
                elif any(x in line for x in ['Profit total', 'Total benefit']):
                    match = re.search(r'([\d.]+)\s*euros?', line)
                    if match:
                        total_benefit = float(match.group(1))
                elif any(x in line for x in ['Time taken', 'Temps d']):
                    match = re.search(r'([\d.]+)\s*seconds?', line)
                    if match:
                        script_time = float(match.group(1))

    except subprocess.TimeoutExpired:
        execution_time = 600
        status = "timeout"
        error_message = "Script timeout (>10 min)"
        print("⏱️ Timeout: Script interrompu après 10 minutes")

    except Exception as e:
        execution_time = 0
        status = "failed"
        # Extraire juste le type d'erreur et le message, pas le traceback
        error_type = type(e).__name__
        error_message = f"{error_type}: {str(e)[:100]}"
        print(f"💥 {error_message}")

    # Enregistrer dans le CSV
    with open(log_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                timestamp,
                script_name,
                script_path,
                dataset_used,
                f"{execution_time:.4f}",
                status,
                error_message,
            ]
        )

    # Résumé
    print(f"\n{'='*60}")
    print(f"⏱️  Temps d'exécution: {execution_time:.4f} secondes")
    print(f"📊 Dataset: {dataset_used}")
    print(f"📊 Status: {status}")
    print(f"📝 Log enregistré dans: {log_csv}")
    print(f"{'='*60}\n")

    return {
        "script_name": script_name,
        "dataset_used": dataset_used,
        "execution_time": execution_time,
        "status": status,
        "output": result.stdout if "result" in locals() else "",
        "error": error_message,
        "total_price": total_price,
        "total_benefit": total_benefit,
        "script_time": script_time,
    }


def load_sienna_decisions():
    """
    Charge les décisions d'achat de Sienna depuis les fichiers texte.

    Returns:
        dict: Dictionnaire avec les résultats de Sienna par dataset
    """
    sienna_results = {}

    # Dataset 1
    file1 = "data/Decisions_achat_1.txt"
    if os.path.exists(file1):
        try:
            with open(file1, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extraire coût et profit
                cost_match = re.search(r'Total cost:\s*([\d.]+)', content)
                profit_match = re.search(r'Total return:\s*([\d.]+)', content)
                if cost_match and profit_match:
                    sienna_results['dataset_1'] = {
                        'price': float(cost_match.group(1)),
                        'benefit': float(profit_match.group(1))
                    }
        except Exception:
            pass

    # Dataset 2
    file2 = "data/Decisions-achat-2.txt"
    if os.path.exists(file2):
        try:
            with open(file2, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extraire coût et profit
                cost_match = re.search(r'Total cost:\s*([\d.]+)', content)
                profit_match = re.search(r'Profit:\s*([\d.]+)', content)
                if cost_match and profit_match:
                    sienna_results['dataset_2'] = {
                        'price': float(cost_match.group(1)),
                        'benefit': float(profit_match.group(1))
                    }
        except Exception:
            pass

    return sienna_results


def test_all_scripts(
    scripts_dir="Scripts",
    log_csv="data/speed_test_records.csv"
):
    """
    Teste tous les scripts Python d'un répertoire.

    Args:
        scripts_dir (str): Répertoire contenant les scripts.
        log_csv (str): Fichier CSV de logs.
    """

    if not os.path.exists(scripts_dir):
        print(f"❌ Le répertoire '{scripts_dir}' n'existe pas.")
        return

    scripts = [f for f in os.listdir(scripts_dir) if f.endswith(".py")]

    if not scripts:
        print(f"❌ Aucun script Python trouvé dans '{scripts_dir}'")
        return

    print(f"\n🔍 {len(scripts)} script(s) trouvé(s) dans '{scripts_dir}':")
    for script in scripts:
        print(f"   - {script}")
    print()

    results = []
    for script in scripts:
        script_path = os.path.join(scripts_dir, script)
        result = measure_script_execution(script_path, log_csv)
        if result:
            results.append(result)
        time.sleep(0.5)

    # Charger les décisions de Sienna
    sienna_data = load_sienna_decisions()

    # Résumé final
    print(f"\n{'='*155}")
    print("📊 RÉSUMÉ DES EXÉCUTIONS")
    print(f"{'='*155}")
    header = (
        f"{'Script':<25} {'Dataset':<20} {'Temps (s)':>12} "
        f"{'T.Script(s)':>13} {'Status':>10} {'Prix (€)':>12} "
        f"{'Bénéfice (€)':>15} {'Δ Sienna (€)':>15}"
    )
    print(header)
    print("-" * 155)
    for r in results:
        price = f"{r['total_price']:.2f}" if r.get('total_price') else "-"
        benefit = f"{r['total_benefit']:.2f}" if r.get('total_benefit') else "-"
        s_time = f"{r['script_time']:.4f}" if r.get('script_time') else "-"

        # Calculer la différence avec Sienna
        delta_str = "-"
        dataset_key = r['dataset_used'].replace('.csv', '')
        if dataset_key in sienna_data and r.get('total_benefit'):
            delta = r['total_benefit'] - sienna_data[dataset_key]['benefit']
            delta_str = f"{delta:+.2f}"

        print(
            f"{r['script_name']:<25} "
            f"{r['dataset_used']:<20} "
            f"{r['execution_time']:>12.4f} "
            f"{s_time:>13} "
            f"{r['status']:>10} "
            f"{price:>12} "
            f"{benefit:>15} "
            f"{delta_str:>15}"
        )

    # Afficher les résultats de Sienna en bas
    if sienna_data:
        print("-" * 155)
        print("\n📋 Décisions d'achat de Sienna (référence):")
        for key, data in sienna_data.items():
            price = data['price']
            benefit = data['benefit']
            print(f"   • {key}: {price:.2f}€ → {benefit:.2f}€ de bénéfice")

    print(f"\n{'='*155}\n")


def show_usage():
    """Affiche l'aide d'utilisation."""
    print("Usage: python speed_test.py [options]")
    print("Options:")
    print("  --all            Tester tous les scripts du dossier Scripts/")
    print("  <script_path>    Tester un script spécifique")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            test_all_scripts()
        elif os.path.exists(sys.argv[1]):
            measure_script_execution(sys.argv[1])
        else:
            show_usage()
    else:
        # Par défaut, on lance tout si aucun argument n'est fourni
        # Ou on affiche l'aide. Pour le confort, lançons --all
        print("Aucun argument fourni. Lancement du test complet...")
        test_all_scripts()
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║           MESURE DE PERFORMANCE D'EXÉCUTION DE SCRIPTS                  ║
╚══════════════════════════════════════════════════════════════════════════╝

Usage:
    python speed_test.py <script_path>
    python speed_test.py --all
    python speed_test.py --help

Exemples:
    # Mesurer un script spécifique
    python speed_test.py Scripts/brute_force.py!
    # Mesurer tous les scripts du dossier Scripts
    python speed_test.py --all

    # Afficher cette aide
    python speed_test.py --help

Les résultats sont automatiquement enregistrés dans:
    data/speed_test_records.csv
    """)


def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        print("❌ Erreur: Aucun argument fourni.\n")
        show_usage()
        sys.exit(1)

    arg = sys.argv[1]

    # Aide
    if arg in ["--help", "-h", "help"]:
        show_usage()
        sys.exit(0)

    # Tester tous les scripts
    if arg == "--all":
        test_all_scripts()
        sys.exit(0)

    # Tester un script spécifique
    script_path = arg

    # Si le chemin est relatif, essayer de le résoudre
    if not os.path.isabs(script_path):
        if not os.path.exists(script_path):
            alt_path = os.path.join("Scripts", script_path)
            if os.path.exists(alt_path):
                script_path = alt_path

    result = measure_script_execution(script_path)

    if result and result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
