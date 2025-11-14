import sys
sys.path.insert(0, 'auth_service')
import app

# inicializa DB limpa
app.DATABASE = 'auth_service.db'
app.init_db()
client = app.app.test_client()
resp = client.post('/register', data='{"username":"testuser","email":"test@example.com","password":"test123"}', content_type='application/json')
print('status', resp.status_code)
print('body', resp.data.decode())
