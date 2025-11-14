import requests
users = ['testuser','user1','user2']
for u in users:
    r = requests.post('http://localhost:5000/register', json={'username':u,'email':f'{u}@example.com','password':'pass123'})
    print(u, r.status_code, r.text)
