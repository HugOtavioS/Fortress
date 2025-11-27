"""
Utilitários para comunicação com os serviços backend
"""
import requests
from django.conf import settings
from typing import Optional, Dict, Any


class AuthServiceClient:
    """Cliente para comunicação com o Auth Service"""
    
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL
    
    def register(self, username: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Registra um novo usuário"""
        try:
            response = requests.post(
                f'{self.base_url}/register',
                json={'username': username, 'email': email, 'password': password},
                timeout=5
            )
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Faz login e retorna token"""
        try:
            response = requests.post(
                f'{self.base_url}/login',
                json={'username': username, 'password': password},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica um token JWT"""
        try:
            response = requests.post(
                f'{self.base_url}/verify',
                json={'token': token},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None


class PasswordManagerServiceClient:
    """Cliente para comunicação com o Password Manager Service"""
    
    def __init__(self):
        self.base_url = settings.PASSWORD_MANAGER_SERVICE_URL
    
    def _get_headers(self, token: str) -> Dict[str, str]:
        """Retorna headers com token de autorização"""
        return {'Authorization': f'Bearer {token}'}
    
    def list_passwords(self, token: str) -> Optional[Dict[str, Any]]:
        """Lista todas as senhas do usuário"""
        try:
            response = requests.get(
                f'{self.base_url}/passwords',
                headers=self._get_headers(token),
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def get_password(self, password_id: int, token: str) -> Optional[Dict[str, Any]]:
        """Obtém uma senha específica"""
        try:
            response = requests.get(
                f'{self.base_url}/passwords/{password_id}',
                headers=self._get_headers(token),
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def create_password(self, site: str, username: str, password: str, token: str) -> Optional[Dict[str, Any]]:
        """Cria uma nova senha"""
        try:
            response = requests.post(
                f'{self.base_url}/passwords',
                json={'site': site, 'username': username, 'password': password},
                headers=self._get_headers(token),
                timeout=5
            )
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def update_password(self, password_id: int, site: str, username: str, 
                       password: str, token: str) -> Optional[Dict[str, Any]]:
        """Atualiza uma senha"""
        try:
            response = requests.put(
                f'{self.base_url}/passwords/{password_id}',
                json={'site': site, 'username': username, 'password': password},
                headers=self._get_headers(token),
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    def delete_password(self, password_id: int, token: str) -> bool:
        """Deleta uma senha"""
        try:
            response = requests.delete(
                f'{self.base_url}/passwords/{password_id}',
                headers=self._get_headers(token),
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

