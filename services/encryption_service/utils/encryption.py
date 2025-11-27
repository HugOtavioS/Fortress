"""
Utilitários para criptografia usando Fernet
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional


class EncryptionService:
    """Serviço de criptografia usando Fernet"""
    
    def __init__(self, key_path: str = 'fernet_key.key'):
        self.key_path = key_path
        self._fernet = None
        self._load_or_generate_key()
    
    def _load_or_generate_key(self):
        """Carrega chave existente ou gera uma nova"""
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:
                key = f.read()
        else:
            # Gera nova chave
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(key)
        
        self._fernet = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Criptografa um texto
        
        Args:
            plaintext: Texto a ser criptografado
            
        Returns:
            Texto criptografado em base64
        """
        if not plaintext:
            raise ValueError("Texto não pode ser vazio")
        
        encrypted_bytes = self._fernet.encrypt(plaintext.encode())
        return encrypted_bytes.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Descriptografa um texto
        
        Args:
            ciphertext: Texto criptografado em base64
            
        Returns:
            Texto descriptografado
        """
        if not ciphertext:
            raise ValueError("Texto criptografado não pode ser vazio")
        
        try:
            decrypted_bytes = self._fernet.decrypt(ciphertext.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar: {str(e)}")


# Instância global do serviço de criptografia
_encryption_service: Optional[EncryptionService] = None


def get_encryption_service(key_path: str = 'fernet_key.key') -> EncryptionService:
    """Obtém instância do serviço de criptografia (singleton)"""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService(key_path)
    return _encryption_service

