import requests


print('Создание пользователя:')
response = requests.put(
    'http://localhost:5000/user/nikita',
    {'password': 'fsdv4w5#'}
)
print(response.json())

print('Создание пользователя с таким же паролем:')
response = requests.put(
    'http://localhost:5000/user/artem',
    {'password': 'fsdv4w5#'}
)
print(response.json())

print('Попытка создать пользователя с уже существующим именем:')
response = requests.put(
    'http://localhost:5000/user/nikita',
    {'password': '3456oijUYr'}
)
print(response.json())

print('Получение данных о пользователе:')
response = requests.get('http://localhost:5000/user/nikita')
print(response.json())

print('Удаление пользователя:')
response = requests.delete('http://localhost:5000/user/nikita')
print(response.text)

print('Попытка получить информацию о несуществующем пользователе:')
response = requests.get('http://localhost:5000/user/nikita')
print(response.json())