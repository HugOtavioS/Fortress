"""
Configurações do Password Manager Service
"""
import os

class Config:
    """Configurações da aplicação"""
    DATABASE = os.getenv('PM_DB_PATH', 'password_manager.db')
    PORT = int(os.getenv('PM_PORT', 5001))
    HOST = os.getenv('PM_HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # URLs dos outros serviços
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5000')
    ENCRYPTION_SERVICE_URL = os.getenv('ENCRYPTION_SERVICE_URL', 'http://localhost:5002')

