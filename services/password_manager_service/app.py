"""
Serviço de Gerenciamento de Senhas - Gerenciador de Senhas
Responsável pelo CRUD de senhas
"""
import sys
from pathlib import Path

# Adicionar diretório pai ao path para permitir importações absolutas quando executado diretamente
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from flask import Flask
from config import Config
from models.password import PasswordRepository
from routes.password_routes import password_bp

app = Flask(__name__)

# Registra blueprint
app.register_blueprint(password_bp)

# Inicializa banco de dados
password_repo = PasswordRepository(Config.DATABASE)


def init_db():
    """Inicializa o banco de dados"""
    password_repo.init_database()


if __name__ == '__main__':
    init_db()
    print(f"🔑 Serviço de Gerenciamento de Senhas iniciado na porta {Config.PORT}")
    print(f"📍 Acesse: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

