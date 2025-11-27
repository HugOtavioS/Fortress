"""
Modelo de Password
"""
from datetime import datetime
import sqlite3
from typing import Optional, Dict, Any, List


class Password:
    """Classe para representar uma senha armazenada"""
    
    def __init__(self, password_id: int, user_id: int, site: str, 
                 username: str, encrypted_password: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = password_id
        self.user_id = user_id
        self.site = site
        self.username = username
        self.encrypted_password = encrypted_password
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a senha para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'site': self.site,
            'username': self.username,
            'encrypted_password': self.encrypted_password,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Password':
        """Cria um objeto Password a partir de uma linha do banco de dados"""
        password_id, user_id, site, username, encrypted_password, created_at, updated_at = row
        return cls(
            password_id=password_id,
            user_id=user_id,
            site=site,
            username=username,
            encrypted_password=encrypted_password,
            created_at=datetime.fromisoformat(created_at) if created_at else None,
            updated_at=datetime.fromisoformat(updated_at) if updated_at else None
        )


class PasswordRepository:
    """Repositório para operações de banco de dados de senhas"""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtém conexão com o banco de dados"""
        return sqlite3.connect(self.database_path)
    
    def create_password(self, user_id: int, site: str, username: str, 
                       encrypted_password: str) -> int:
        """Cria uma nova senha e retorna o ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO passwords (user_id, site, username, encrypted_password)
                   VALUES (?, ?, ?, ?)''',
                (user_id, site, username, encrypted_password)
            )
            password_id = cursor.lastrowid
            conn.commit()
            return password_id
        finally:
            conn.close()
    
    def get_password_by_id(self, password_id: int, user_id: int) -> Optional[Password]:
        """Busca senha por ID (apenas se pertencer ao usuário)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''SELECT id, user_id, site, username, encrypted_password, 
                          created_at, updated_at 
                   FROM passwords 
                   WHERE id = ? AND user_id = ?''',
                (password_id, user_id)
            )
            row = cursor.fetchone()
            if row:
                return Password.from_db_row(row)
            return None
        finally:
            conn.close()
    
    def get_all_passwords(self, user_id: int) -> List[Password]:
        """Busca todas as senhas de um usuário"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''SELECT id, user_id, site, username, encrypted_password, 
                          created_at, updated_at 
                   FROM passwords 
                   WHERE user_id = ? 
                   ORDER BY site, username''',
                (user_id,)
            )
            rows = cursor.fetchall()
            return [Password.from_db_row(row) for row in rows]
        finally:
            conn.close()
    
    def update_password(self, password_id: int, user_id: int, site: str,
                        username: str, encrypted_password: str) -> bool:
        """Atualiza uma senha"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''UPDATE passwords 
                   SET site = ?, username = ?, encrypted_password = ?, 
                       updated_at = CURRENT_TIMESTAMP
                   WHERE id = ? AND user_id = ?''',
                (site, username, encrypted_password, password_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_password(self, password_id: int, user_id: int) -> bool:
        """Deleta uma senha"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'DELETE FROM passwords WHERE id = ? AND user_id = ?',
                (password_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, site, username)
                )
            ''')
            conn.commit()
        finally:
            conn.close()

