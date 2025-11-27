"""
Configurações do Encryption Service
"""
import os

class Config:
    """Configurações da aplicação"""
    PORT = int(os.getenv('ENCRYPTION_PORT', 5002))
    HOST = os.getenv('ENCRYPTION_HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    FERNET_KEY_PATH = os.getenv('FERNET_KEY_PATH', 'fernet_key.key')

