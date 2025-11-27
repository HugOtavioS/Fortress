"""
Rotas do Encryption Service
"""
from flask import Blueprint, request, jsonify
from utils.encryption import get_encryption_service
from config import Config

encryption_bp = Blueprint('encryption', __name__)
encryption_service = get_encryption_service(Config.FERNET_KEY_PATH)


@encryption_bp.route('/encrypt', methods=['POST'])
def encrypt():
    """Endpoint para criptografar senha"""
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Campo "password" é obrigatório'}), 400
        
        password = data['password']
        
        if not password:
            return jsonify({'error': 'Senha não pode ser vazia'}), 400
        
        try:
            encrypted = encryption_service.encrypt(password)
            return jsonify({
                'encrypted_password': encrypted
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@encryption_bp.route('/decrypt', methods=['POST'])
def decrypt():
    """Endpoint para descriptografar senha"""
    try:
        data = request.get_json()
        
        if not data or 'encrypted_password' not in data:
            return jsonify({'error': 'Campo "encrypted_password" é obrigatório'}), 400
        
        encrypted_password = data['encrypted_password']
        
        if not encrypted_password:
            return jsonify({'error': 'Senha criptografada não pode ser vazia'}), 400
        
        try:
            decrypted = encryption_service.decrypt(encrypted_password)
            return jsonify({
                'password': decrypted
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@encryption_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'OK',
        'service': 'encryption_service',
        'version': '1.0.0'
    }), 200

