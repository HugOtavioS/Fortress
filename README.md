# 🔐 Gerenciador de Senhas - Projeto Escolar

Um sistema completo de gerenciamento de senhas desenvolvido com arquitetura de microsserviços usando Python, Flask e Django. O projeto permite que usuários se cadastrem, façam login e gerenciem suas senhas de forma segura com criptografia.

## 🏗️ Arquitetura do Sistema

O projeto utiliza uma arquitetura baseada em microsserviços leves:

- **Auth Service** (Porta 5000): Gerencia autenticação e autorização de usuários
- **Encryption Service** (Porta 5002): Responsável pela criptografia/descriptografia de senhas
- **Password Manager Service** (Porta 5001): Gerencia CRUD de senhas
- **Frontend Django** (Porta 8000): Interface web para interação com os serviços

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Frontend**: Django, HTML, CSS
- **Banco de Dados**: SQLite
- **Criptografia**: cryptography (Fernet)
- **Autenticação**: JWT (PyJWT)
- **Testes**: pytest, locust
- **Versionamento**: Git

## 📁 Estrutura do Projeto

```
project_root/
├── services/                     # Microsserviços Flask
│   ├── auth_service/            # Serviço de Autenticação
│   │   ├── app.py              # Aplicação Flask principal
│   │   ├── config.py           # Configurações
│   │   ├── models/             # Modelos de dados
│   │   │   └── user.py
│   │   ├── routes/             # Rotas da API
│   │   │   └── auth_routes.py
│   │   ├── utils/              # Utilitários
│   │   │   ├── password.py
│   │   │   └── jwt_token.py
│   │   └── tests/             # Testes unitários
│   │       └── test_auth.py
│   ├── encryption_service/      # Serviço de Criptografia
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   └── encryption_routes.py
│   │   ├── utils/
│   │   │   └── encryption.py
│   │   └── tests/
│   │       └── test_encryption.py
│   └── password_manager_service/  # Serviço de Gerenciamento de Senhas
│       ├── app.py
│       ├── config.py
│       ├── models/
│       │   └── password.py
│       ├── routes/
│       │   └── password_routes.py
│       ├── utils/
│       │   ├── auth_client.py
│       │   └── encryption_client.py
│       └── tests/
├── frontend_django/            # Frontend Django
│   ├── manage.py
│   ├── password_manager/      # Configurações do projeto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── password_app/          # Aplicação Django
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── utils.py
│   └── templates/            # Templates HTML
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── add_password.html
│       └── edit_password.html
├── tests/                     # Testes de integração e carga
│   ├── integration/
│   │   └── test_integration.py
│   └── load/
├── scripts/                   # Scripts utilitários
│   └── debug/                # Scripts de debug
├── requirements.txt          # Dependências Python
├── setup_project.py         # Script de configuração inicial
├── init_django_manual.py     # Script de inicialização do Django
├── run_tests.py             # Script para executar todos os testes
├── check_services.py        # Script para verificar status dos serviços
├── start_services.sh        # Script para iniciar serviços (Linux/Mac)
├── start_services.bat       # Script para iniciar serviços (Windows)
└── README.md               # Este arquivo
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para versionamento)

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd fortress
```

### 2. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac (POPOS, Ubuntu, etc.)
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Inicialize o Django (IMPORTANTE)

**Execute este comando ANTES de iniciar os serviços:**

```bash
# Linux/Mac (POPOS, Ubuntu, etc.)
python3 init_django_manual.py

# Windows
python init_django_manual.py
```

Este comando cria as tabelas necessárias do Django, incluindo a tabela `django_session`.

### 5. Inicie os Serviços

**Opção 1 - Script Automático:**
- Windows: `start_services.bat` (usa `python -m` internamente)
- Linux/Mac: `./start_services.sh` (usa `python -m` internamente)

**Opção 2 - Manual (4 terminais separados):**

Observação: para evitar o erro "attempted relative import with no known parent package", execute os serviços como módulos a partir da raiz do projeto usando `-m`.

**Terminal 1 - Auth Service:**
```bash
cd auth_service
python3 app.py
```

**Terminal 2 - Encryption Service:**
```bash
cd encryption_service
python3 app.py
```

**Terminal 3 - Password Manager Service:**
```bash
cd password_manager_service
python3 app.py
```

**Terminal 4 - Frontend Django:**
```bash
cd frontend_django
python3 manage.py runserver
```

### 6. Acesse a Aplicação

Abra seu navegador e acesse: `http://localhost:8000`

## 🧪 Executando os Testes

### Testes Unitários

```bash
# Testes do Auth Service
cd services/auth_service
python3 -m pytest tests/ -v

# Testes do Encryption Service
cd services/encryption_service
python3 -m pytest tests/ -v

# Testes do Password Manager Service
cd services/password_manager_service
python3 -m pytest tests/ -v
```

### Testes de Integração

```bash
# Certifique-se de que todos os serviços estão rodando
python3 -m pytest tests/integration/ -v

# Ou use o script de testes
python3 run_tests.py
```

### Testes de Carga

```bash
# Instale o locust se ainda não estiver instalado
pip install locust

# Execute os testes de carga
cd tests/load
locust -f test_load.py --host=http://localhost:5001
```

Acesse `http://localhost:8089` para visualizar a interface do Locust.

## 🔧 Funcionalidades

### Para Usuários

1. **Cadastro**: Crie uma conta com username, email e senha
2. **Login**: Acesse sua conta com username e senha
3. **Dashboard**: Visualize todas as suas senhas armazenadas
4. **Adicionar Senha**: Armazene senhas para sites/serviços
5. **Editar Senha**: Atualize informações de senhas existentes
6. **Deletar Senha**: Remova senhas que não são mais necessárias
7. **Visualizar Senha**: Veja a senha descriptografada (com botão de mostrar/ocultar)

### Características de Segurança

- Senhas de usuários são hasheadas com SHA-256
- Senhas armazenadas são criptografadas com Fernet (AES 128)
- Autenticação baseada em JWT com expiração de 24 horas
- Isolamento de dados entre usuários
- Validação de entrada em todos os endpoints

## 📊 APIs Disponíveis

### Auth Service (Porta 5000)

- `POST /register` - Cadastro de usuário
- `POST /login` - Login de usuário
- `POST /verify` - Verificação de token
- `GET /health` - Health check

### Encryption Service (Porta 5002)

- `POST /encrypt` - Criptografar senha
- `POST /decrypt` - Descriptografar senha
- `GET /health` - Health check

### Password Manager Service (Porta 5001)

- `GET /passwords` - Listar senhas do usuário
- `POST /passwords` - Criar nova senha
- `GET /passwords/{id}` - Obter senha específica
- `PUT /passwords/{id}` - Atualizar senha
- `DELETE /passwords/{id}` - Deletar senha
- `GET /health` - Health check

## 🗄️ Banco de Dados

O projeto utiliza SQLite para simplicidade. Cada serviço possui seu próprio banco:

- `auth_service.db` - Dados de usuários
- `password_manager.db` - Senhas criptografadas
- `db.sqlite3` - Banco do Django (se necessário)

## 🔒 Segurança

- **Criptografia**: Todas as senhas são criptografadas usando Fernet (AES 128)
- **Hash de Senhas**: Senhas de usuários são hasheadas com SHA-256
- **JWT**: Tokens de autenticação com expiração automática
- **Validação**: Validação rigorosa de entrada em todos os endpoints
- **Isolamento**: Cada usuário só acessa suas próprias senhas

## 🚀 Deploy em Produção

Para deploy em produção, considere:

1. **Variáveis de Ambiente**: Use variáveis de ambiente para chaves secretas
2. **HTTPS**: Configure SSL/TLS para comunicação segura
3. **Banco de Dados**: Migre para PostgreSQL ou MySQL
4. **Proxy Reverso**: Use Nginx ou Apache como proxy reverso
5. **Monitoramento**: Implemente logs e monitoramento
6. **Backup**: Configure backup regular dos bancos de dados

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🐛 Solução de Problemas

### Erro "no such table: django_session"

**Solução:** Execute o comando de inicialização do Django:

```bash
# Linux/Mac (POPOS, Ubuntu, etc.)
python3 init_django_manual.py

# Windows
python init_django_manual.py
```

Ou manualmente:

```bash
cd frontend_django
# Linux/Mac
python3 manage.py migrate
# Windows
python manage.py migrate
```

### Erro de Porta em Uso

Se alguma porta estiver em uso, altere a porta no arquivo `config.py` do serviço correspondente ou use variáveis de ambiente:

```bash
export AUTH_PORT=5000
export PM_PORT=5001
export ENCRYPTION_PORT=5002
```

### Erro de Dependências

Se houver problemas com dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de Banco de Dados

Se houver problemas com o banco de dados, delete os arquivos `.db` e reinicie os serviços:

```bash
rm *.db
# Reinicie os serviços
```

### Erro de CSRF no Django

Se houver erros de CSRF, as views já estão configuradas com `@csrf_exempt` para desenvolvimento.

### Ordem de Inicialização

**IMPORTANTE:** Sempre execute nesta ordem:

1. `python3 init_django_manual.py` (apenas uma vez) - Linux/Mac
   `python init_django_manual.py` - Windows
2. Inicie os serviços Flask (Auth, Encryption, Password Manager)
3. Inicie o Django (`python3 manage.py runserver` - Linux/Mac, `python manage.py runserver` - Windows)

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs dos serviços
2. Execute os testes para identificar problemas
3. Consulte a documentação das bibliotecas utilizadas
4. Abra uma issue no repositório

---

**Desenvolvido para fins educacionais** 🎓

Este projeto foi criado como exemplo de arquitetura de microsserviços e boas práticas de desenvolvimento em Python.
