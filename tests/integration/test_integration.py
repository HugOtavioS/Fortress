"""
Testes de integração entre os serviços
"""
import pytest
import requests
import time
import sys
import os

# URLs dos serviços
AUTH_SERVICE_URL = 'http://localhost:5000'
ENCRYPTION_SERVICE_URL = 'http://localhost:5002'
PASSWORD_MANAGER_SERVICE_URL = 'http://localhost:5001'


def wait_for_service(url, timeout=30):
    """Aguarda um serviço ficar disponível"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


@pytest.fixture(scope="session")
def services_ready():
    """Verifica se todos os serviços estão rodando"""
    services = [
        (AUTH_SERVICE_URL, "Auth Service"),
        (ENCRYPTION_SERVICE_URL, "Encryption Service"),
        (PASSWORD_MANAGER_SERVICE_URL, "Password Manager Service"),
    ]
    
    all_ready = True
    for url, name in services:
        if not wait_for_service(url):
            print(f"⚠️  {name} não está disponível em {url}")
            all_ready = False
    
    if not all_ready:
        pytest.skip("Alguns serviços não estão disponíveis. Inicie todos os serviços antes de executar os testes.")
    
    return True


@pytest.fixture
def test_user(services_ready):
    """Cria um usuário de teste"""
    username = f"testuser_{int(time.time())}"
    email = f"{username}@test.com"
    password = "test123456"
    
    response = requests.post(
        f"{AUTH_SERVICE_URL}/register",
        json={'username': username, 'email': email, 'password': password},
        timeout=5
    )
    
    if response.status_code == 201:
        data = response.json()
        yield {
            'username': username,
            'email': email,
            'password': password,
            'token': data['token'],
            'user_id': data['user_id']
        }
    else:
        pytest.fail(f"Falha ao criar usuário de teste: {response.text}")


def test_auth_service_health(services_ready):
    """Testa health check do Auth Service"""
    response = requests.get(f"{AUTH_SERVICE_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'OK'


def test_encryption_service_health(services_ready):
    """Testa health check do Encryption Service"""
    response = requests.get(f"{ENCRYPTION_SERVICE_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'OK'


def test_password_manager_service_health(services_ready):
    """Testa health check do Password Manager Service"""
    response = requests.get(f"{PASSWORD_MANAGER_SERVICE_URL}/health", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'OK'


def test_register_and_login_flow(services_ready):
    """Testa fluxo completo de registro e login"""
    username = f"testuser_{int(time.time())}"
    email = f"{username}@test.com"
    password = "test123456"
    
    # Registro
    register_response = requests.post(
        f"{AUTH_SERVICE_URL}/register",
        json={'username': username, 'email': email, 'password': password},
        timeout=5
    )
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert 'token' in register_data
    
    # Login
    login_response = requests.post(
        f"{AUTH_SERVICE_URL}/login",
        json={'username': username, 'password': password},
        timeout=5
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert 'token' in login_data
    assert login_data['username'] == username


def test_encryption_flow(services_ready):
    """Testa fluxo de criptografia e descriptografia"""
    password = "minha_senha_secreta_123"
    
    # Criptografa
    encrypt_response = requests.post(
        f"{ENCRYPTION_SERVICE_URL}/encrypt",
        json={'password': password},
        timeout=5
    )
    assert encrypt_response.status_code == 200
    encrypted = encrypt_response.json()['encrypted_password']
    assert encrypted != password
    
    # Descriptografa
    decrypt_response = requests.post(
        f"{ENCRYPTION_SERVICE_URL}/decrypt",
        json={'encrypted_password': encrypted},
        timeout=5
    )
    assert decrypt_response.status_code == 200
    decrypted = decrypt_response.json()['password']
    assert decrypted == password


def test_password_crud_flow(services_ready, test_user):
    """Testa fluxo completo de CRUD de senhas"""
    token = test_user['token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Cria senha
    create_response = requests.post(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords",
        json={'site': 'test.com', 'username': 'testuser', 'password': 'testpass123'},
        headers=headers,
        timeout=5
    )
    assert create_response.status_code == 201
    password_id = create_response.json()['id']
    
    # Lista senhas
    list_response = requests.get(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords",
        headers=headers,
        timeout=5
    )
    assert list_response.status_code == 200
    passwords = list_response.json()['passwords']
    assert len(passwords) > 0
    
    # Obtém senha específica
    get_response = requests.get(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords/{password_id}",
        headers=headers,
        timeout=5
    )
    assert get_response.status_code == 200
    password_data = get_response.json()
    assert password_data['site'] == 'test.com'
    
    # Atualiza senha
    update_response = requests.put(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords/{password_id}",
        json={'site': 'test.com', 'username': 'testuser', 'password': 'newpass123'},
        headers=headers,
        timeout=5
    )
    assert update_response.status_code == 200
    
    # Deleta senha
    delete_response = requests.delete(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords/{password_id}",
        headers=headers,
        timeout=5
    )
    assert delete_response.status_code == 200


def test_end_to_end_flow(services_ready):
    """Testa fluxo completo end-to-end"""
    username = f"e2e_user_{int(time.time())}"
    email = f"{username}@test.com"
    password = "test123456"
    
    # 1. Registro
    register_response = requests.post(
        f"{AUTH_SERVICE_URL}/register",
        json={'username': username, 'email': email, 'password': password},
        timeout=5
    )
    assert register_response.status_code == 201
    token = register_response.json()['token']
    
    # 2. Cria senha criptografada
    headers = {'Authorization': f'Bearer {token}'}
    create_response = requests.post(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords",
        json={'site': 'example.com', 'username': 'user@example.com', 'password': 'mypassword123'},
        headers=headers,
        timeout=5
    )
    assert create_response.status_code == 201
    password_id = create_response.json()['id']
    
    # 3. Verifica que a senha foi armazenada
    list_response = requests.get(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords",
        headers=headers,
        timeout=5
    )
    assert list_response.status_code == 200
    passwords = list_response.json()['passwords']
    assert len(passwords) == 1
    assert passwords[0]['site'] == 'example.com'
    
    # 4. Obtém e verifica que a senha descriptografada está correta
    get_response = requests.get(
        f"{PASSWORD_MANAGER_SERVICE_URL}/passwords/{password_id}",
        headers=headers,
        timeout=5
    )
    assert get_response.status_code == 200
    password_data = get_response.json()
    assert password_data['password'] == 'mypassword123'

