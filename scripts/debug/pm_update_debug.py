import sys
sys.path.insert(0, 'password_manager_service')
import app
from unittest.mock import Mock, patch
import json

app.app.config['TESTING'] = True
with app.app.app_context():
    app.init_db()

# Mock verify (first call) and encrypt (second call)
mock_auth = Mock(); mock_auth.json.return_value = {'valid': True, 'user_id': 1, 'username':'testuser', 'email':'test@example.com'}; mock_auth.status_code = 200
mock_encrypt = Mock(); mock_encrypt.json.return_value = {'encrypted_password': 'encrypted_test123'}; mock_encrypt.status_code = 200

# Simulate create
with patch('requests.get') as mock_get:
    mock_get.return_value.json.return_value = {'passwords': []}
    mock_get.return_value.status_code = 200
    with patch('requests.post') as mock_create_post:
        mock_create_auth = Mock(); mock_create_auth.json.return_value = {'valid': True, 'user_id':1}; mock_create_auth.status_code = 200
        mock_create_encrypt = Mock(); mock_create_encrypt.json.return_value = {'encrypted_password': 'encrypted123'}; mock_create_encrypt.status_code = 200
        mock_create_post.side_effect = [mock_create_auth, mock_create_encrypt]
        client = app.app.test_client()
        create_data = {'site':'test.com','username':'testuser','password':'test123'}
        r = client.post('/passwords', headers={'Authorization':'valid_token'}, data=json.dumps(create_data), content_type='application/json')
        print('create status', r.status_code, r.data.decode())

# Now perform update with patched requests.post for verify+encrypt
with patch('requests.post') as mock_post:
    mock_post.side_effect = [mock_auth, mock_encrypt]
    client = app.app.test_client()
    update_data = {'site':'updated.com','username':'updateduser','password':'newpassword123'}
    r2 = client.put('/passwords/1', headers={'Authorization':'valid_token'}, data=json.dumps(update_data), content_type='application/json')
    print('update status', r2.status_code)
    print('update body', r2.data.decode())

# Inspect DB
import sqlite3
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()
cursor.execute('SELECT id,user_id,site,username,encrypted_password,notes FROM passwords')
rows = cursor.fetchall()
print('db rows:', rows)
conn.close()
