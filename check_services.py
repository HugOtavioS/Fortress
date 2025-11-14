#!/usr/bin/env python3
"""
Script para verificar se todos os serviços estão funcionando
"""
import requests
import time
import sys

def check_service(url, service_name):
    """Verifica se um serviço está funcionando"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {service_name}: {data.get('status', 'OK')}")
            return True
        else:
            print(f"❌ {service_name}: Erro HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name}: Serviço não está rodando")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {service_name}: Timeout na conexão")
        return False
    except Exception as e:
        print(f"❌ {service_name}: Erro - {e}")
        return False

def main():
    """Função principal"""
    print("🔍 Verificando Status dos Serviços")
    print("=" * 40)
    
    services = [
        ("http://localhost:5000", "Auth Service"),
        ("http://localhost:5001", "Password Manager Service"),
        ("http://localhost:5002", "Encryption Service"),
        ("http://localhost:8000", "Django Frontend")
    ]
    
    all_ok = True
    
    for url, name in services:
        if not check_service(url, name):
            all_ok = False
    
    print("\n" + "=" * 40)
    if all_ok:
        print("🎉 Todos os serviços estão funcionando!")
        print("Acesse: http://localhost:8000")
    else:
        print("⚠️  Alguns serviços não estão funcionando.")
        print("Verifique se todos os serviços foram iniciados corretamente.")
        print("\nPara iniciar os serviços:")
        print("- Windows: start_services.bat")
        print("- Linux/Mac: ./start_services.sh")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())



