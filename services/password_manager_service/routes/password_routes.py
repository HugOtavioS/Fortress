"""
Rotas do Password Manager Service
"""
from flask import Blueprint, request, jsonify
from models.password import PasswordRepository
from utils.auth_client import AuthClient
from utils.encryption_client import EncryptionClient
from config import Config

password_bp = Blueprint('password', __name__)
password_repo = PasswordRepository(Config.DATABASE)
auth_client = AuthClient()
encryption_client = EncryptionClient()


def get_user_id_from_token():
    """
    Extrai e valida o token do header Authorization
    
    Returns:
        Tupla (sucesso, user_id, resposta_erro, status_code)
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header:
        return False, 0, (jsonify({'error': 'Token de autorização não fornecido'}), 401)
    
    # Formato esperado: "Bearer <token>"
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0] != 'Bearer':
        return False, 0, (jsonify({'error': 'Formato de token inválido. Use: Bearer <token>'}), 401)
    
    token = parts[1]
    user_data = auth_client.verify_token(token)
    
    if not user_data:
        return False, 0, (jsonify({'error': 'Token inválido ou expirado'}), 401)
    
    return True, user_data['user_id'], None


@password_bp.route('/passwords', methods=['GET'])
def list_passwords():
    """Endpoint para listar todas as senhas do usuário"""
    try:
        result = get_user_id_from_token()
        success, user_id, error_response = result[0], result[1], result[2]
        if not success:
            return error_response[0], error_response[1]
        
        passwords = password_repo.get_all_passwords(user_id)
        
        return jsonify({
            'passwords': [p.to_dict() for p in passwords],
            'count': len(passwords)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@password_bp.route('/passwords', methods=['POST'])
def create_password():
    """Endpoint para criar uma nova senha"""
    try:
        result = get_user_id_from_token()
        success, user_id, error_response = result[0], result[1], result[2]
        if not success:
            return error_response[0], error_response[1]
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        site = data.get('site', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not site:
            return jsonify({'error': 'Campo "site" é obrigatório'}), 400
        
        if not username:
            return jsonify({'error': 'Campo "username" é obrigatório'}), 400
        
        if not password:
            return jsonify({'error': 'Campo "password" é obrigatório'}), 400
        
        # Criptografa a senha
        encrypted_password = encryption_client.encrypt(password)
        if not encrypted_password:
            return jsonify({'error': 'Erro ao criptografar senha'}), 500
        
        try:
            password_id = password_repo.create_password(
                user_id, site, username, encrypted_password
            )
            
            return jsonify({
                'message': 'Senha criada com sucesso',
                'id': password_id
            }), 201
            
        except Exception as e:
            if 'UNIQUE' in str(e):
                return jsonify({'error': 'Já existe uma senha para este site e username'}), 400
            raise
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@password_bp.route('/passwords/<int:password_id>', methods=['GET'])
def get_password(password_id):
    """Endpoint para obter uma senha específica"""
    try:
        result = get_user_id_from_token()
        success, user_id, error_response = result[0], result[1], result[2]
        if not success:
            return error_response[0], error_response[1]
        
        password = password_repo.get_password_by_id(password_id, user_id)
        
        if not password:
            return jsonify({'error': 'Senha não encontrada'}), 404
        
        # Descriptografa a senha para retornar
        decrypted_password = encryption_client.decrypt(password.encrypted_password)
        if not decrypted_password:
            return jsonify({'error': 'Erro ao descriptografar senha'}), 500
        
        password_dict = password.to_dict()
        password_dict['password'] = decrypted_password
        
        return jsonify(password_dict), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@password_bp.route('/passwords/<int:password_id>', methods=['PUT'])
def update_password(password_id):
    """Endpoint para atualizar uma senha"""
    try:
        result = get_user_id_from_token()
        success, user_id, error_response = result[0], result[1], result[2]
        if not success:
            return error_response[0], error_response[1]
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        site = data.get('site', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not site:
            return jsonify({'error': 'Campo "site" é obrigatório'}), 400
        
        if not username:
            return jsonify({'error': 'Campo "username" é obrigatório'}), 400
        
        if not password:
            return jsonify({'error': 'Campo "password" é obrigatório'}), 400
        
        # Verifica se a senha existe e pertence ao usuário
        existing_password = password_repo.get_password_by_id(password_id, user_id)
        if not existing_password:
            return jsonify({'error': 'Senha não encontrada'}), 404
        
        # Criptografa a nova senha
        encrypted_password = encryption_client.encrypt(password)
        if not encrypted_password:
            return jsonify({'error': 'Erro ao criptografar senha'}), 500
        
        # Atualiza
        success = password_repo.update_password(
            password_id, user_id, site, username, encrypted_password
        )
        
        if not success:
            return jsonify({'error': 'Erro ao atualizar senha'}), 500
        
        return jsonify({'message': 'Senha atualizada com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@password_bp.route('/passwords/<int:password_id>', methods=['DELETE'])
def delete_password(password_id):
    """Endpoint para deletar uma senha"""
    try:
        result = get_user_id_from_token()
        success, user_id, error_response = result[0], result[1], result[2]
        if not success:
            return error_response[0], error_response[1]
        
        success = password_repo.delete_password(password_id, user_id)
        
        if not success:
            return jsonify({'error': 'Senha não encontrada'}), 404
        
        return jsonify({'message': 'Senha deletada com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@password_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'OK',
        'service': 'password_manager_service',
        'version': '1.0.0'
    }), 200

