import subprocess, sys, time, requests
procs=[]
try:
    procs.append(subprocess.Popen([sys.executable, 'auth_service/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    procs.append(subprocess.Popen([sys.executable, 'encryption_service/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    procs.append(subprocess.Popen([sys.executable, 'password_manager_service/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    print('Started services, waiting...')
    time.sleep(3)
    def reg(u,p):
        r = requests.post('http://localhost:5000/register', json={'username':u, 'email':f'{u}@example.com','password':p})
        print('register',u,r.status_code,r.text)
        return r
    r1=reg('user1','pass123')
    r2=reg('user2','pass456')
    def create(u,token,site,usern,pwd):
        r = requests.post('http://localhost:5001/passwords', headers={'Authorization':token}, json={'site':site,'username':usern,'password':pwd})
        print('create',u,r.status_code,r.text)
        return r
    t1 = r1.json().get('token') if r1.status_code==201 else requests.post('http://localhost:5000/login', json={'username':'user1','password':'pass123'}).json().get('token')
    t2 = r2.json().get('token') if r2.status_code==201 else requests.post('http://localhost:5000/login', json={'username':'user2','password':'pass456'}).json().get('token')
    create('user1', t1, 'user1site.com','user1','user1pass')
    create('user2', t2, 'user2site.com','user2','user2pass')
    r1_list = requests.get('http://localhost:5001/passwords', headers={'Authorization':t1})
    r2_list = requests.get('http://localhost:5001/passwords', headers={'Authorization':t2})
    print('list1', r1_list.status_code, r1_list.text)
    print('list2', r2_list.status_code, r2_list.text)
finally:
    for p in procs:
        try:
            p.terminate()
        except Exception:
            pass
