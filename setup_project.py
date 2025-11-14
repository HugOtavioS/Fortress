#!/usr/bin/env python3
"""
Script de configuração inicial do projeto
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    print(f"Executando: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Falhou: {e}")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def create_virtual_environment():
    """Cria ambiente virtual"""
    if os.path.exists("venv"):
        print("✅ Ambiente virtual já existe")
        return True
    
    return run_command("python -m venv venv", "Criando ambiente virtual")

def activate_virtual_environment():
    """Ativa ambiente virtual"""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"Para ativar o ambiente virtual, execute: {activate_script}")
    return True

def install_dependencies():
    """Instala dependências do projeto"""
    if platform.system() == "Windows":
        pip_command = "venv\\Scripts\\pip"
    else:
        pip_command = "venv/bin/pip"
    
    commands = [
        f"{pip_command} install --upgrade pip",
        f"{pip_command} install -r requirements.txt"
    ]
    
    for command in commands:
        if not run_command(command, f"Executando: {command}"):
            return False
    return True

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        "auth_service/tests",
        "encryption_service/tests", 
        "password_manager_service/tests",
        "tests",
        "frontend_django/templates",
        "frontend_django/static"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Diretório criado: {directory}")
    
    return True

def create_git_repository():
    """Inicializa repositório Git"""
    if os.path.exists(".git"):
        print("✅ Repositório Git já existe")
        return True
    
    commands = [
        "git init",
        "git add .",
        'git commit -m "Initial commit - Gerenciador de Senhas"'
    ]
    
    for command in commands:
        if not run_command(command, f"Git: {command}"):
            return False
    return True

def main():
    """Função principal de configuração"""
    print("🔧 Configurando Projeto Gerenciador de Senhas")
    print("=" * 50)
    
    # Verificações iniciais
    if not check_python_version():
        return 1
    
    # Configuração do projeto
    steps = [
        ("Criando diretórios", create_directories),
        ("Criando ambiente virtual", create_virtual_environment),
        ("Instalando dependências", install_dependencies),
        ("Inicializando Git", create_git_repository)
    ]
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            print(f"❌ Falha na etapa: {step_name}")
            return 1
    
    # Instruções finais
    print("\n" + "=" * 50)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("\nPróximos passos:")
    print("1. Ative o ambiente virtual:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Inicie os serviços:")
    if platform.system() == "Windows":
        print("   start_services.bat")
    else:
        print("   ./start_services.sh")
    
    print("\n3. Acesse a aplicação:")
    print("   http://localhost:8000")
    
    print("\n4. Execute os testes:")
    print("   python run_tests.py")
    
    print("\n📚 Consulte o README.md para mais informações")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())



