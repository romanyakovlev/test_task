# Тестовое задание

Проект залит на [heroku](http://sheltered-harbor-24371.herokuapp.com/). БД - PostgreSQL.

# Работа с API

Выдает меню ресторана в JSON формате:

```sh
http://sheltered-harbor-24371.herokuapp.com/api/menu/ 
```
Создает заказ:

```sh
http://sheltered-harbor-24371.herokuapp.com/api/create_order/1+1+2?operator=Вася
```
где "1+1+2" - id блюд, "operator=Вася" - идентификатор оператора. Авторизация проходит через HTTP Basic Auth.

# Зависимости
- flask
- requests
- flask-admin
- flask-httpauth
- flask-babelex
- flask-login
- flask-sqlalchemy
- psycopg2
- sqlalchemy_mptt


