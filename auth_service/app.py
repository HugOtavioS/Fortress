"""
Serviço de Autenticação - Gerenciador de Senhas
Responsável por cadastro e login de usuários
"""

from flask import Flask, request, jsonify
import sqlite3
import hashlib
import jwt
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-para-jwt'  # Em produção, usar variável de ambiente

# Configuração do banco de dados
DATABASE = 'auth_service.db'

class User:
    """Classe para representar um usuário"""
    
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
    
    def to_dict(self):
        """Converte o usuário para dicionário"""
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

def init_db():
    """Inicializa o banco de dados"""
    # Garante que começamos com um DB limpo ao iniciar o serviço
    try:
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
    except Exception:
        pass

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
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
    conn.close()

def hash_password(password):
    """Gera hash da senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verifica se a senha está correta"""
    return hash_password(password) == password_hash

def generate_token(user_id):
    """Gera token JWT para o usuário"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verifica e decodifica o token JWT"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/register', methods=['POST'])
def register():
    """Endpoint para cadastro de usuário"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Validações básicas
        if len(password) < 6:
            return jsonify({'error': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # Hash da senha
        password_hash = hash_password(password)
        
        # Conecta ao banco
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            # Insere usuário
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            
            # Gera token
            token = generate_token(user_id)
            
            return jsonify({
                'message': 'Usuário cadastrado com sucesso',
                'token': token,
                'user_id': user_id
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Usuário ou email já existem'}), 400
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuário"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username e senha são obrigatórios'}), 400
        
        username = data['username']
        password = data['password']
        
        # Conecta ao banco
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Busca usuário
        cursor.execute(
            'SELECT id, username, email, password_hash FROM users WHERE username = ?',
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        user_id, db_username, email, password_hash = user
        
        # Verifica senha
        if not verify_password(password, password_hash):
            return jsonify({'error': 'Senha incorreta'}), 401
        
        # Gera token
        token = generate_token(user_id)
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'token': token,
            'user_id': user_id,
            'username': db_username,
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/verify', methods=['POST'])
def verify():
    """Endpoint para verificar token"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({'error': 'Token é obrigatório'}), 400
        
        token = data['token']
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        # Busca dados do usuário
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT username, email FROM users WHERE id = ?',
            (user_id,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        username, email = user
        
        return jsonify({
            'valid': True,
            'user_id': user_id,
            'username': username,
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'OK', 'service': 'auth_service'}), 200

if __name__ == '__main__':
    init_db()
    print("Serviço de Autenticação iniciado na porta 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)


