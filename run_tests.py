#!/usr/bin/env python3
"""
Script para executar todos os testes do projeto
"""
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    print(f"\n{'='*50}")
    print(f"Executando: {description}")
    print(f"Comando: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("ERRO:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 Executando Testes do Gerenciador de Senhas")
    print("=" * 60)
    
    # Lista de testes para executar
    tests = [
        {
            "command": "cd services/auth_service && python3 -m pytest tests/ -v",
            "description": "Testes Unitários - Auth Service"
        },
        {
            "command": "cd services/encryption_service && python3 -m pytest tests/ -v",
            "description": "Testes Unitários - Encryption Service"
        },
        {
            "command": "cd services/password_manager_service && python3 -m pytest tests/ -v",
            "description": "Testes Unitários - Password Manager Service"
        },
        {
            "command": "python3 -m pytest tests/integration/ -v",
            "description": "Testes de Integração"
        }
    ]
    
    # Executa os testes
    passed = 0
    total = len(tests)
    
    for test in tests:
        if run_command(test["command"], test["description"]):
            passed += 1
            print("✅ PASSOU")
        else:
            print("❌ FALHOU")
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"RESUMO DOS TESTES")
    print(f"{'='*60}")
    print(f"Testes executados: {total}")
    print(f"Testes passaram: {passed}")
    print(f"Testes falharam: {total - passed}")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam!")
        return 1

if __name__ == "__main__":
    sys.exit(main())



