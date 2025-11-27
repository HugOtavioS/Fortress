"""
Cliente para comunicação com o Auth Service
"""
import requests
from typing import Optional, Dict, Any
from config import Config


class AuthClient:
    """Cliente para verificação de tokens com o Auth Service"""
    
    def __init__(self, auth_service_url: str = None):
        self.auth_service_url = auth_service_url or Config.AUTH_SERVICE_URL
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica um token JWT com o Auth Service
        
        Args:
            token: Token JWT a ser verificado
            
        Returns:
            Dicionário com dados do usuário se válido, None caso contrário
        """
        try:
            response = requests.post(
                f'{self.auth_service_url}/verify',
                json={'token': token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    return data
            return None
        except requests.exceptions.RequestException:
            return None
    
    def get_user_id(self, token: str) -> Optional[int]:
        """
        Obtém o ID do usuário a partir do token
        
        Args:
            token: Token JWT
            
        Returns:
            ID do usuário ou None se inválido
        """
        user_data = self.verify_token(token)
        if user_data:
            return user_data.get('user_id')
        return None

