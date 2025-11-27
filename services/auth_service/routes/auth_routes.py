"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify
from models.user import UserRepository
from utils.password import hash_password, verify_password, validate_password
from utils.jwt_token import generate_token, verify_token
from config import Config
import sqlite3

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository(Config.DATABASE)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para cadastro de usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validações
        if not username:
            return jsonify({'error': 'Username é obrigatório'}), 400
        
        if not email:
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        if not password:
            return jsonify({'error': 'Senha é obrigatória'}), 400
        
        # Valida senha
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Valida email básico
        if '@' not in email:
            return jsonify({'error': 'Email inválido'}), 400
        
        # Hash da senha
        password_hash = hash_password(password)
        
        try:
            # Cria usuário
            user_id = user_repo.create_user(username, email, password_hash)
            
            # Gera token
            token = generate_token(user_id)
            
            return jsonify({
                'message': 'Usuário cadastrado com sucesso',
                'token': token,
                'user_id': user_id
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Usuário ou email já existem'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username:
            return jsonify({'error': 'Username é obrigatório'}), 400
        
        if not password:
            return jsonify({'error': 'Senha é obrigatória'}), 400
        
        # Busca usuário
        user = user_repo.get_user_by_username(username)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Verifica senha
        if not verify_password(password, user.password_hash):
            return jsonify({'error': 'Senha incorreta'}), 401
        
        # Gera token
        token = generate_token(user.id)
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@auth_bp.route('/verify', methods=['POST'])
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
        user = user_repo.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'valid': True,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@auth_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'OK',
        'service': 'auth_service',
        'version': '1.0.0'
    }), 200

