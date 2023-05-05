# Flask-приложение "Обьявления"

Для создания БД запустить команду:
```
docker-compose up -d
```
Создать файл .env, по примеру:
```
PG_USER='login'
PG_PASSWORD='password'
PG_DB='name_db'
SECRET_KEY='you_secret_key'
```
Для создания таблиц:
```
python models.py
```
Для запуска сервера:
```
python server.py
```
Для проверки:
```
python client.py
```