"""
Configurações do Auth Service
"""
import os

class Config:
    """Configurações da aplicação"""
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'chave-secreta-para-jwt')
    DATABASE = os.getenv('AUTH_DB_PATH', 'auth_service.db')
    PORT = int(os.getenv('AUTH_PORT', 5000))
    HOST = os.getenv('AUTH_HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))

