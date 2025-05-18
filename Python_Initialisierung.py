import os
import subprocess

# Standard .gitignore Inhalt für Python-Projekte
GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
.venv/
env/
venv/

# VSCode settings
.vscode/

# Distribution / packaging
build/
dist/
*.egg-info/

# dotenv
.env
"""

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, shell=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

def create_project(project_name):
    base_path = os.getcwd()
    project_path = os.path.join(base_path, project_name)

    if os.path.exists(project_path):
        print(f"Fehler: Ordner '{project_name}' existiert bereits!")
        return

    os.makedirs(project_path)

    # .gitignore schreiben
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.write(GITIGNORE_CONTENT.strip())

    # README.md schreiben
    readme_content = f"# {project_name}\n\n## Beschreibung\n\nKurze Projektbeschreibung.\n\n## Setup\n\n```bash\npython -m venv venv\nsource venv/bin/activate  # oder .\\venv\\Scripts\\activate auf Windows\npip install -r requirements.txt\n```\n\n## Verwendung\n\nKurzes Beispiel, wie man das Projekt nutzt.\n\n## Lizenz\n\nMIT License\n"
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(readme_content)

    # Git initialisieren
    run_command("git init", cwd=project_path)

    # venv erstellen
    run_command("python -m venv venv", cwd=project_path)

    # pip freeze > requirements.txt in der venv
    pip_path = os.path.join(project_path, "venv", "Scripts" if os.name == "nt" else "bin", "pip")
    freeze_cmd = f"{pip_path} freeze > requirements.txt"
    run_command(freeze_cmd, cwd=project_path)

    # Dateien zu git hinzufügen
    run_command("git add .", cwd=project_path)
    run_command('git commit -m "Initial commit"', cwd=project_path)

    # GitHub-Repo mit GitHub CLI erstellen und pushen
    run_command(f"gh repo create {project_name} --public --source=. --remote=origin --push", cwd=project_path)

    print(f"Projekt '{project_name}' wurde erfolgreich erstellt und gepusht!")

def main():
    project_name = input("Wie soll dein Projekt heißen? ").strip()

    if not project_name:
        print("Abgebrochen: Kein Projektname angegeben.")
        return

    confirm = input(f"Projekt '{project_name}' jetzt initialisieren? (j/n): ").strip().lower()
    if confirm == "j":
        create_project(project_name)
    else:
        print("Abgebrochen.")

if __name__ == "__main__":
    main()