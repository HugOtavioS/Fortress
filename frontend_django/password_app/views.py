"""
Views do Django para o gerenciador de senhas
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import AuthServiceClient, PasswordManagerServiceClient


auth_client = AuthServiceClient()
pm_client = PasswordManagerServiceClient()


def get_token_from_session(request):
    """Obtém token da sessão"""
    return request.session.get('token')


def set_token_in_session(request, token):
    """Armazena token na sessão"""
    request.session['token'] = token


def clear_session(request):
    """Limpa a sessão"""
    request.session.flush()


def require_auth(view_func):
    """Decorator para exigir autenticação"""
    def wrapper(request, *args, **kwargs):
        token = get_token_from_session(request)
        if not token:
            return redirect('login')
        
        # Verifica se o token ainda é válido
        user_data = auth_client.verify_token(token)
        if not user_data:
            clear_session(request)
            return redirect('login')
        
        request.user_data = user_data
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(["GET", "POST"])
def login_view(request):
    """View de login"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            return render(request, 'login.html', {
                'error': 'Username e senha são obrigatórios'
            })
        
        result = auth_client.login(username, password)
        
        if result:
            set_token_in_session(request, result['token'])
            request.session['user_id'] = result['user_id']
            request.session['username'] = result['username']
            request.session['email'] = result['email']
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Credenciais inválidas'
            })
    
    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """View de registro"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not username or not email or not password:
            return render(request, 'register.html', {
                'error': 'Todos os campos são obrigatórios'
            })
        
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'As senhas não coincidem'
            })
        
        result = auth_client.register(username, email, password)
        
        if result:
            set_token_in_session(request, result['token'])
            request.session['user_id'] = result['user_id']
            return redirect('dashboard')
        else:
            return render(request, 'register.html', {
                'error': 'Erro ao registrar. Usuário ou email já existem.'
            })
    
    return render(request, 'register.html')


@require_http_methods(["GET"])
def logout_view(request):
    """View de logout"""
    clear_session(request)
    return redirect('login')


@require_http_methods(["GET"])
@require_auth
def dashboard_view(request):
    """View do dashboard"""
    token = get_token_from_session(request)
    passwords_data = pm_client.list_passwords(token)
    
    passwords = passwords_data.get('passwords', []) if passwords_data else []
    
    return render(request, 'dashboard.html', {
        'passwords': passwords,
        'username': request.session.get('username', '')
    })


@require_http_methods(["GET", "POST"])
@require_auth
def add_password_view(request):
    """View para adicionar senha"""
    if request.method == 'POST':
        site = request.POST.get('site', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not site or not username or not password:
            return render(request, 'add_password.html', {
                'error': 'Todos os campos são obrigatórios'
            })
        
        token = get_token_from_session(request)
        result = pm_client.create_password(site, username, password, token)
        
        if result:
            return redirect('dashboard')
        else:
            return render(request, 'add_password.html', {
                'error': 'Erro ao criar senha. Tente novamente.'
            })
    
    return render(request, 'add_password.html')


@require_http_methods(["GET", "POST"])
@require_auth
def edit_password_view(request, password_id):
    """View para editar senha"""
    token = get_token_from_session(request)
    
    if request.method == 'POST':
        site = request.POST.get('site', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not site or not username or not password:
            password_data = pm_client.get_password(password_id, token)
            return render(request, 'edit_password.html', {
                'error': 'Todos os campos são obrigatórios',
                'password': password_data
            })
        
        result = pm_client.update_password(password_id, site, username, password, token)
        
        if result:
            return redirect('dashboard')
        else:
            password_data = pm_client.get_password(password_id, token)
            return render(request, 'edit_password.html', {
                'error': 'Erro ao atualizar senha. Tente novamente.',
                'password': password_data
            })
    
    password_data = pm_client.get_password(password_id, token)
    
    if not password_data:
        return redirect('dashboard')
    
    return render(request, 'edit_password.html', {
        'password': password_data
    })


@require_http_methods(["POST"])
@require_auth
def delete_password_view(request, password_id):
    """View para deletar senha"""
    token = get_token_from_session(request)
    success = pm_client.delete_password(password_id, token)
    
    if success:
        return redirect('dashboard')
    else:
        return render(request, 'dashboard.html', {
            'error': 'Erro ao deletar senha',
            'passwords': pm_client.list_passwords(token).get('passwords', []) if pm_client.list_passwords(token) else []
        })

