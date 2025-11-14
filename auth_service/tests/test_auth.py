"""
Testes unitários para o serviço de autenticação
"""
import pytest
import json
import os
import tempfile
from app import app, init_db, hash_password, verify_password, generate_token, verify_token

@pytest.fixture
def client():
    """Cliente de teste para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            yield client

def test_hash_password():
    """Testa geração de hash de senha"""
    password = "test123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) == 64  # SHA-256 produces 64 character hex string
    assert hashed == hash_password(password)  # Same password should produce same hash

def test_verify_password():
    """Testa verificação de senha"""
    password = "test123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) == True
    assert verify_password("wrong", hashed) == False

def test_generate_and_verify_token():
    """Testa geração e verificação de token JWT"""
    user_id = 123
    token = generate_token(user_id)
    
    assert token is not None
    assert isinstance(token, str)
    
    decoded_user_id = verify_token(token)
    assert decoded_user_id == user_id

def test_verify_invalid_token():
    """Testa verificação de token inválido"""
    invalid_token = "invalid.token.here"
    result = verify_token(invalid_token)
    assert result is None

def test_register_success(client):
    """Testa registro de usuário com sucesso"""
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    }
    
    response = client.post('/register', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'token' in response_data
    assert 'user_id' in response_data
    assert response_data['message'] == 'Usuário cadastrado com sucesso'

def test_register_duplicate_username(client):
    """Testa registro com username duplicado"""
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    }
    
    # Primeiro registro
    client.post('/register', 
               data=json.dumps(data),
               content_type='application/json')
    
    # Segundo registro com mesmo username
    response = client.post('/register', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'já existem' in response_data['error']

def test_register_missing_data(client):
    """Testa registro com dados faltando"""
    data = {
        'username': 'testuser'
        # Faltando email e password
    }
    
    response = client.post('/register', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'incompletos' in response_data['error']

def test_register_short_password(client):
    """Testa registro com senha muito curta"""
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '123'  # Muito curta
    }
    
    response = client.post('/register', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert '6 caracteres' in response_data['error']

def test_login_success(client):
    """Testa login com sucesso"""
    # Primeiro registra o usuário
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    }
    client.post('/register', 
               data=json.dumps(register_data),
               content_type='application/json')
    
    # Agora faz login
    login_data = {
        'username': 'testuser',
        'password': 'test123'
    }
    
    response = client.post('/login', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'token' in response_data
    assert response_data['username'] == 'testuser'

def test_login_wrong_password(client):
    """Testa login com senha incorreta"""
    # Primeiro registra o usuário
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    }
    client.post('/register', 
               data=json.dumps(register_data),
               content_type='application/json')
    
    # Login com senha errada
    login_data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    
    response = client.post('/login', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 401
    response_data = json.loads(response.data)
    assert 'incorreta' in response_data['error']

def test_login_nonexistent_user(client):
    """Testa login com usuário inexistente"""
    login_data = {
        'username': 'nonexistent',
        'password': 'test123'
    }
    
    response = client.post('/login', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'não encontrado' in response_data['error']

def test_verify_token_success(client):
    """Testa verificação de token válido"""
    # Registra usuário e obtém token
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123'
    }
    response = client.post('/register', 
                          data=json.dumps(register_data),
                          content_type='application/json')
    
    token = json.loads(response.data)['token']
    
    # Verifica token
    verify_data = {'token': token}
    response = client.post('/verify', 
                          data=json.dumps(verify_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['valid'] == True
    assert response_data['username'] == 'testuser'

def test_verify_invalid_token(client):
    """Testa verificação de token inválido"""
    verify_data = {'token': 'invalid.token.here'}
    response = client.post('/verify', 
                          data=json.dumps(verify_data),
                          content_type='application/json')
    
    assert response.status_code == 401
    response_data = json.loads(response.data)
    assert 'inválido' in response_data['error']

def test_health_check(client):
    """Testa endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'OK'
    assert response_data['service'] == 'auth_service'



