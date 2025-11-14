@echo off
echo Iniciando Gerenciador de Senhas - Servicos
echo ==========================================

echo.
echo Configurando Django (executando migracoes)...
cd frontend_django
python init_django.py
cd ..

echo.
echo Iniciando Auth Service (porta 5000)...
start "Auth Service" cmd /k "cd auth_service && python app.py"

timeout /t 2 /nobreak > nul

echo.
echo Iniciando Encryption Service (porta 5002)...
start "Encryption Service" cmd /k "cd encryption_service && python app.py"

timeout /t 2 /nobreak > nul

echo.
echo Iniciando Password Manager Service (porta 5001)...
start "Password Manager Service" cmd /k "cd password_manager_service && python app.py"

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
