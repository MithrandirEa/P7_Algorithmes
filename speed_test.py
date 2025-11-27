"""
Script de mesure de performance d'exécution

Usage:
    python speed_test.py script_to_test.py
    python speed_test.py Scripts/brute_force.py
    python speed_test.py --all
"""

import csv
import os
import subprocess
import sys
import time
from datetime import datetime


def measure_script_execution(
    script_path, log_csv="data/speed_test_records.csv"
):
    """
    Mesure le temps d'exécution d'un script Python et enregistre dans un CSV

    Args:
        script_path (str): Chemin vers le script à exécuter
        log_csv (str): Chemin vers le fichier CSV de logs

    Returns:
        dict: Résultats de l'exécution (temps, status, output)
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
            import re
            csv_matches = re.findall(r'["\']([^"\']*/)?([^/"\']*(dataset|actions)[^"\']*.csv)["\']', script_content, re.IGNORECASE)
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

        result = subprocess.run(
            [sys.executable, script_path],
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
            # Extraire seulement la dernière ligne du stderr (le message d'erreur principal)
            if result.stderr:
                error_lines = result.stderr.strip().split('\n')
                last_line = error_lines[-1][:150]
                # Simplifier le message si c'est un timeout
                if "TimeoutError" in last_line or "Timeout reached" in last_line:
                    error_message = "Timeout"
                else:
                    error_message = last_line
            else:
                error_message = f"Exit code {result.returncode}"
            print(f"❌ Erreur: {error_message}")

        # Afficher la sortie
        if result.stdout:
            print("\n📤 Sortie standard:")
            print(result.stdout)

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
    }


def test_all_scripts(
    scripts_dir="Scripts",
    log_csv="data/speed_test_records.csv"
):
    """
    Teste tous les scripts Python d'un répertoire

    Args:
        scripts_dir (str): Répertoire contenant les scripts
        log_csv (str): Fichier CSV de logs
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

    # Résumé final
    print(f"\n{'='*70}")
    print("📊 RÉSUMÉ DES EXÉCUTIONS")
    print(f"{'='*70}")
    print(f"{'Script':<25} {'Dataset':<20} {'Temps (s)':>12} {'Status':>10}")
    print("-" * 70)
    for r in results:
        print(
            f"{r['script_name']:<25} "
            f"{r['dataset_used']:<20} "
            f"{r['execution_time']:>12.4f} "
            f"{r['status']:>10}"
        )
    print(f"{'='*70}\n")


def show_usage():
    """Affiche l'aide d'utilisation"""
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
