import requests
import json

res = json.loads(requests.post('http://127.0.0.1:5000/api/login', data={'username': 'Neil', 'password': 'abcdefg'}).content.decode())

print("Login :", res)

if res["error"] == "0":
    headers = {'TOKEN': res['token'], 'Referer': 'http://127.0.0.1:5000/api/wel'}
    res = json.loads(requests.post('http://127.0.0.1:5000/api/wel', headers=headers).content.decode())
    print("Welcome :", res)

res = json.loads(requests.post('http://127.0.0.1:5000/api/login', data={'username': 'Neil', 'password': 'abc'}).content.decode())

print("Login :", res)

if res["error"] == "0":
    headers = {'TOKEN': res['token'], 'Referer': 'http://127.0.0.1:5000/api/wel'}
    res = json.loads(requests.post('http://127.0.0.1:5000/api/wel', headers=headers).content.decode())
    print("Welcome :", res)
