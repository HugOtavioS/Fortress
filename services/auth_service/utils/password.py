"""
Utilitários para manipulação de senhas
"""
import hashlib


def hash_password(password: str) -> str:
    """
    Gera hash da senha usando SHA-256
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash hexadecimal da senha
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica se a senha está correta
    
    Args:
        password: Senha em texto plano
        password_hash: Hash da senha armazenado
        
    Returns:
        True se a senha está correta, False caso contrário
    """
    return hash_password(password) == password_hash


def validate_password(password: str) -> tuple[bool, str]:
    """
    Valida se a senha atende aos requisitos
    
    Args:
        password: Senha a ser validada
        
    Returns:
        Tupla (é_válida, mensagem_erro)
    """
    if not password:
        return False, 'Senha é obrigatória'
    
    if len(password) < 6:
        return False, 'Senha deve ter pelo menos 6 caracteres'
    
    if len(password) > 128:
        return False, 'Senha deve ter no máximo 128 caracteres'
    
    return True, ''

