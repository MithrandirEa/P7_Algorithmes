"""
Script de mesure de performance d'exécution

Usage:
    python processing_speed_records.py script_to_test.py
    python processing_speed_records.py Scripts/brute_force.py
    python processing_speed_records.py --all
"""

import csv
import os
import subprocess
import sys
import time
from datetime import datetime


def measure_script_execution(
    script_path, log_csv="first_search/data/processing_speed_records.csv"
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
                    "execution_time_seconds",
                    "status",
                    "error_message",
                ]
            )

    script_name = os.path.basename(script_path)
    timestamp = datetime.now().isoformat()
    error_message = ""

    print(f"\n{'='*60}")
    print(f"🚀 Exécution de: {script_name}")
    print(f"📁 Chemin: {script_path}")
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
            error_message = result.stderr[:200]
            print(f"❌ Erreur d'exécution (code: {result.returncode})")

        # Afficher la sortie
        if result.stdout:
            print("\n📤 Sortie standard:")
            print(result.stdout)

        if result.stderr and status == "error":
            print("\n⚠️ Erreurs:")
            print(result.stderr[:500])

    except subprocess.TimeoutExpired:
        execution_time = 600
        status = "timeout"
        error_message = "Timeout après 10 minutes"
        print("⏱️ Timeout: Le script a dépassé 10 minutes")

    except Exception as e:
        execution_time = 0
        status = "failed"
        error_message = str(e)[:200]
        print(f"💥 Erreur inattendue: {e}")

    # Enregistrer dans le CSV
    with open(log_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                timestamp,
                script_name,
                script_path,
                f"{execution_time:.4f}",
                status,
                error_message,
            ]
        )

    # Résumé
    print(f"\n{'='*60}")
    print(f"⏱️  Temps d'exécution: {execution_time:.4f} secondes")
    print(f"📊 Status: {status}")
    print(f"📝 Log enregistré dans: {log_csv}")
    print(f"{'='*60}\n")

    return {
        "script_name": script_name,
        "execution_time": execution_time,
        "status": status,
        "output": result.stdout if "result" in locals() else "",
        "error": error_message,
    }


def test_all_scripts(
    scripts_dir="Scripts", log_csv="first_search/data/processing_speed_records.csv"
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
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES EXÉCUTIONS")
    print(f"{'='*60}")
    print(f"{'Script':<30} {'Temps (s)':>12} {'Status':>15}")
    print("-" * 60)
    for r in results:
        print(
            f"{r['script_name']:<30} "
            f"{r['execution_time']:>12.4f} "
            f"{r['status']:>15}"
        )
    print(f"{'='*60}\n")


def show_usage():
    """Affiche l'aide d'utilisation"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║           MESURE DE PERFORMANCE D'EXÉCUTION DE SCRIPTS                  ║
╚══════════════════════════════════════════════════════════════════════════╝

Usage:
    python processing_speed_records.py <script_path>
    python processing_speed_records.py --all
    python processing_speed_records.py --help

Exemples:
    # Mesurer un script spécifique
    python processing_speed_records.py Scripts/brute_force.py
    
    # Mesurer tous les scripts du dossier Scripts
    python processing_speed_records.py --all
    
    # Afficher cette aide
    python processing_speed_records.py --help

Les résultats sont automatiquement enregistrés dans:
    first_search/data/processing_speed_records.csv
    """)


def main():
    if len(sys.argv) < 2:
        print("❌ Erreur: Aucun argument fourni.\n")
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