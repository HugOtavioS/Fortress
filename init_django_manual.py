#!/usr/bin/env python3
"""
Script para inicializar o Django manualmente
Execute este script antes de iniciar os serviços
"""
import os
import sys
import subprocess

def run_django_commands():
    """Executa comandos necessários do Django"""
    print("🔧 Inicializando Django...")
    
    # Navega para o diretório do Django
    os.chdir('frontend_django')
    
    commands = [
        ['python', 'manage.py', 'migrate', '--run-syncdb'],
        ['python', 'manage.py', 'migrate'],
    ]
    
    for command in commands:
        print(f"Executando: {' '.join(command)}")
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("✅ Sucesso")
            if result.stdout:
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    print("✅ Django inicializado com sucesso!")
    return True

if __name__ == '__main__':
    success = run_django_commands()
    if success:
        print("\n🎉 Django está pronto! Agora você pode iniciar os serviços.")
    else:
        print("\n❌ Erro ao inicializar Django. Verifique os erros acima.")
        sys.exit(1)



