import requests

response = requests.post('http://127.0.0.1:5000/ad/',
                         json={
                             "title": "Test1",
                             "description": "DescTest1"
                         })
print(response.status_code)
print(response.json())

response = requests.get(f'http://127.0.0.1:5000/ad/{response.json()["id"]}')
print(response.status_code)
print(response.json())

response = requests.patch(f'http://127.0.0.1:5000/ad/{response.json()["id"]}',
                          json={
                              "description": "DescTest2"
                          })
print(response.status_code)
print(response.json())

response = requests.delete(f'http://127.0.0.1:5000/ad/{response.json()["id"]}')
print(response.status_code)


# response = requests.post('http://127.0.0.1:5000/signup',
#                          json={
#                              "username": "User3",
#                              "email": "user3@mail.ru",
#                              "password_hash": "user1pwd"
#                          })
# print(response.status_code)
# print(response.json())


# response = requests.post('http://127.0.0.1:5000/login',
#                          json={
#                              "username": "User3",
#                              "password_hash": "user1pwd"
#                          })
# print(response.status_code)
# print(response.json())
#
# response = requests.get('http://127.0.0.1:5000/log')
