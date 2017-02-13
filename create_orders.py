from requests.auth import HTTPBasicAuth
import requests
import random
from server import restaurant_users, restaurant_dict

operators_list = ['Оператор Вася', 'Оператор Петя', 'Оператор Дима']
orders_list = [[1,2,1,1,1],[2,2,3,1,],[1,1,1,3],[2,3,2,3],[3,3,3,3,1]]
for order_list in orders_list:
    requests.get('http://sheltered-harbor-24371.herokuapp.com/api/create_order/{}'. format(
                        '+'.join(str(x) for x in order_list)),
                        params={'operator': random.choice(operators_list)},
                        auth=HTTPBasicAuth(*random.choice(tuple(restaurant_users.items()))))
