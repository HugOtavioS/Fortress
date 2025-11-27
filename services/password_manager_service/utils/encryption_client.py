"""
Cliente para comunicação com o Encryption Service
"""
import requests
from typing import Optional
from config import Config


class EncryptionClient:
    """Cliente para criptografia/descriptografia com o Encryption Service"""
    
    def __init__(self, encryption_service_url: str = None):
        self.encryption_service_url = encryption_service_url or Config.ENCRYPTION_SERVICE_URL
    
    def encrypt(self, password: str) -> Optional[str]:
        """
        Criptografa uma senha
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Senha criptografada ou None em caso de erro
        """
        try:
            response = requests.post(
                f'{self.encryption_service_url}/encrypt',
                json={'password': password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('encrypted_password')
            return None
        except requests.exceptions.RequestException:
            return None
    
    def decrypt(self, encrypted_password: str) -> Optional[str]:
        """
        Descriptografa uma senha
        
        Args:
            encrypted_password: Senha criptografada
            
        Returns:
            Senha descriptografada ou None em caso de erro
        """
        try:
            response = requests.post(
                f'{self.encryption_service_url}/decrypt',
                json={'encrypted_password': encrypted_password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('password')
            return None
        except requests.exceptions.RequestException:
            return None

