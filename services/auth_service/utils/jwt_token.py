"""
Utilitários para manipulação de tokens JWT
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional
from config import Config


def generate_token(user_id: int) -> str:
    """
    Gera token JWT para o usuário
    
    Args:
        user_id: ID do usuário
        
    Returns:
        Token JWT codificado
    """
    payload = {
        'user_id': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> Optional[int]:
    """
    Verifica e decodifica o token JWT
    
    Args:
        token: Token JWT a ser verificado
        
    Returns:
        ID do usuário se o token for válido, None caso contrário
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

