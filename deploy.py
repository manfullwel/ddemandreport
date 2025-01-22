import os
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {command}")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error executing {command}")
        print(e.stderr)
        exit(1)

def main():
    # Configurações
    repo_url = "https://github.com/manfullwel/ddemandreport.git"
    branch = "master"
    
    # Comandos git
    commands = [
        "git add .",
        'git commit -m "feat: Add CI/CD pipeline and tests"',
        f"git remote set-url origin {repo_url}",
        f"git push -u origin {branch}"
    ]
    
    print("[START] Iniciando deploy...")
    
    # Executa cada comando
    for cmd in commands:
        run_command(cmd)
    
    print("[DONE] Deploy concluido com sucesso!")

if __name__ == "__main__":
    main()
