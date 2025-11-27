"""
Serviço de Criptografia - Gerenciador de Senhas
Responsável pela criptografia e descriptografia de senhas
"""
import sys
from pathlib import Path

# Adicionar diretório pai ao path para permitir importações absolutas quando executado diretamente
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from flask import Flask
from config import Config
from routes.encryption_routes import encryption_bp

app = Flask(__name__)

# Registra blueprint
app.register_blueprint(encryption_bp)


if __name__ == '__main__':
    print(f"🔐 Serviço de Criptografia iniciado na porta {Config.PORT}")
    print(f"📍 Acesse: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

