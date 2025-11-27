@echo off
echo Iniciando Gerenciador de Senhas - Servicos
echo ==========================================

REM Move para o diretório do script (raiz do projeto) para que imports relativos
REM funcionem quando executamos como módulos com -m
pushd "%~dp0"

echo.
echo Configurando Django (executando migracoes)...
cd frontend_django
python manage.py migrate
cd ..

echo.
echo Iniciando Auth Service (porta 5000)...
start "Auth Service" cmd /k "python -m services.auth_service.app"

timeout /t 2 /nobreak > nul

echo.
echo Iniciando Encryption Service (porta 5002)...
start "Encryption Service" cmd /k "python -m services.encryption_service.app"

timeout /t 2 /nobreak > nul

echo.
echo Iniciando Password Manager Service (porta 5001)...
start "Password Manager Service" cmd /k "python -m services.password_manager_service.app"

timeout /t 2 /nobreak > nul

echo.
echo Iniciando Frontend Django (porta 8000)...
start "Django Frontend" cmd /k "cd frontend_django && python manage.py runserver"

echo.
echo ==========================================
echo Todos os servicos foram iniciados!
echo.
echo Acesse: http://localhost:8000
echo.
echo Para parar os servicos, feche as janelas do terminal.
echo ==========================================
pause

REM Retorna para diretório anterior
popd
