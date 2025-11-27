"""
Testes unitários para o serviço de criptografia
"""
import pytest
import json
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.encryption import EncryptionService


@pytest.fixture
def client():
    """Cliente de teste para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def encryption_service(tmp_path):
    """Cria uma instância do serviço de criptografia para testes"""
    key_path = tmp_path / 'test_key.key'
    return EncryptionService(str(key_path))


def test_encrypt_decrypt(encryption_service):
    """Testa criptografia e descriptografia"""
    plaintext = "minha_senha_secreta_123"
    
    encrypted = encryption_service.encrypt(plaintext)
    assert encrypted != plaintext
    assert len(encrypted) > 0
    
    decrypted = encryption_service.decrypt(encrypted)
    assert decrypted == plaintext


def test_encrypt_empty_string(encryption_service):
    """Testa criptografia de string vazia"""
    with pytest.raises(ValueError):
        encryption_service.encrypt("")


def test_decrypt_invalid_string(encryption_service):
    """Testa descriptografia de string inválida"""
    with pytest.raises(ValueError):
        encryption_service.decrypt("invalid_ciphertext")


def test_encrypt_endpoint(client):
    """Testa endpoint de criptografia"""
    data = {'password': 'test_password_123'}
    
    response = client.post('/encrypt',
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'encrypted_password' in response_data
    assert response_data['encrypted_password'] != data['password']


def test_decrypt_endpoint(client):
    """Testa endpoint de descriptografia"""
    # Primeiro criptografa
    encrypt_data = {'password': 'test_password_123'}
    encrypt_response = client.post('/encrypt',
                                  data=json.dumps(encrypt_data),
                                  content_type='application/json')
    encrypted = json.loads(encrypt_response.data)['encrypted_password']
    
    # Depois descriptografa
    decrypt_data = {'encrypted_password': encrypted}
    decrypt_response = client.post('/decrypt',
                                  data=json.dumps(decrypt_data),
                                  content_type='application/json')
    
    assert decrypt_response.status_code == 200
    response_data = json.loads(decrypt_response.data)
    assert response_data['password'] == encrypt_data['password']


def test_encrypt_missing_field(client):
    """Testa endpoint de criptografia sem campo obrigatório"""
    data = {}
    
    response = client.post('/encrypt',
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'obrigatório' in response_data['error']


def test_decrypt_missing_field(client):
    """Testa endpoint de descriptografia sem campo obrigatório"""
    data = {}
    
    response = client.post('/decrypt',
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'obrigatório' in response_data['error']


def test_health_check(client):
    """Testa endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['status'] == 'OK'
    assert response_data['service'] == 'encryption_service'

