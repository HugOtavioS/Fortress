#!/bin/bash

echo "Iniciando Gerenciador de Senhas - Serviços"
echo "=========================================="

echo ""
echo "Configurando Django (executando migrações)..."
cd frontend_django
python3 manage.py migrate
cd ..

echo ""
echo "Iniciando Auth Service (porta 5000)..."
gnome-terminal --title="Auth Service" -- bash -c "cd services/auth_service && python3 app.py; exec bash" &

sleep 2

echo ""
echo "Iniciando Encryption Service (porta 5002)..."
gnome-terminal --title="Encryption Service" -- bash -c "cd services/encryption_service && python3 app.py; exec bash" &

sleep 2

echo ""
echo "Iniciando Password Manager Service (porta 5001)..."
gnome-terminal --title="Password Manager Service" -- bash -c "cd services/password_manager_service && python3 app.py; exec bash" &

sleep 2

echo ""
echo "Iniciando Frontend Django (porta 8000)..."
gnome-terminal --title="Django Frontend" -- bash -c "cd frontend_django && python3 manage.py runserver; exec bash" &

echo ""
echo "=========================================="
echo "Todos os serviços foram iniciados!"
echo ""
echo "Acesse: http://localhost:8000"
echo ""
echo "Para parar os serviços, feche as janelas do terminal."
echo "=========================================="
