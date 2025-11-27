import sys
sys.path.insert(0, 'password_manager_service')
import app
from types import SimpleNamespace

# Ensure testing config and clean DB
app.app.config['TESTING'] = True
with app.app.app_context():
    app.init_db()

# Mock requests.post to simulate auth verification then encryption
class MockResp:
    def __init__(self, json_data, status):
        self._json = json_data
        self.status_code = status
    def json(self):
        return self._json

calls = []
def mock_post(url, json=None):
    calls.append((url, json))
    if url.endswith('/verify'):
        return MockResp({'valid': True, 'user_id': 1, 'username': 'testuser', 'email': 'test@example.com'}, 200)
    if url.endswith('/encrypt'):
        return MockResp({'encrypted_password': 'encrypted_test123'}, 200)
    return MockResp({}, 500)

import requests
requests.post = mock_post

client = app.app.test_client()
req_data = {'site':'test.com','username':'testuser','password':'test123','notes':'Test notes'}
resp = client.post('/passwords', headers={'Authorization':'valid_token'}, data=app.json.dumps(req_data), content_type='application/json')
print('status', resp.status_code)
print('body', resp.data.decode())
print('requests calls:', calls)
