"""
Modelo de Usuário
"""
from datetime import datetime
import sqlite3
from typing import Optional, Dict, Any


class User:
    """Classe para representar um usuário"""
    
    def __init__(self, user_id: int, username: str, email: str, 
                 password_hash: str, created_at: Optional[datetime] = None):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o usuário para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'User':
        """Cria um objeto User a partir de uma linha do banco de dados"""
        user_id, username, email, password_hash, created_at = row
        return cls(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=datetime.fromisoformat(created_at) if created_at else None
        )


class UserRepository:
    """Repositório para operações de banco de dados de usuários"""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtém conexão com o banco de dados"""
        return sqlite3.connect(self.database_path)
    
    def create_user(self, username: str, email: str, password_hash: str) -> int:
        """Cria um novo usuário e retorna o ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT id, username, email, password_hash, created_at FROM users WHERE username = ?',
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return User.from_db_row(row)
            return None
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT id, username, email, password_hash, created_at FROM users WHERE id = ?',
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return User.from_db_row(row)
            return None
        finally:
            conn.close()
    
    def init_database(self, reset: bool = False):
        """Inicializa o banco de dados"""
        import os
        if reset and os.path.exists(self.database_path):
            try:
                os.remove(self.database_path)
            except Exception:
                pass
        
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        finally:
            conn.close()

