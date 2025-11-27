"""
Serviço de Autenticação - Gerenciador de Senhas
Responsável por cadastro e login de usuários
"""
import sys
from pathlib import Path

# Adicionar diretório pai ao path para permitir importações absolutas quando executado diretamente
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from flask import Flask
from config import Config
from models.user import UserRepository
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Registra blueprint
app.register_blueprint(auth_bp)

# Inicializa banco de dados
user_repo = UserRepository(Config.DATABASE)


def init_db(reset: bool = False):
    """Inicializa o banco de dados"""
    user_repo.init_database(reset=reset)


if __name__ == '__main__':
    init_db(reset=False)
    print(f"🚀 Serviço de Autenticação iniciado na porta {Config.PORT}")
    print(f"📍 Acesse: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
