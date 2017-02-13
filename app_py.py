from models import Product, Category, User, Order
from flask import render_template, make_response, jsonify, redirect, request
from make_menu import root
from flask_admin import Admin
from flask_httpauth import HTTPBasicAuth
from views import MyModelView, MyAdminIndexView, StatisticView, ProductModelView, \
    CategoryModelView, UserModelView, OrderModelView
from flask_babelex import Babel
from settings import app, db
import flask_login as login
import os

auth = HTTPBasicAuth()
babel = Babel(app)

restaurant_users = {
    'Burger1': 'admin1',
    'Burger2': 'admin2'
}

restaurant_dict = {
    'Burger1':'Бургер "Б" №1',
    'Burger2':'Бургер "Б" №2'
}


@babel.localeselector
def get_locale():
        return 'ru'


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@auth.get_password
def get_password(username):
    if username in restaurant_users.keys():
        return restaurant_users[username]
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def index():
    return redirect('/admin/')


@app.route('/api/menu')
@auth.login_required
def menu_api():
    return jsonify(root)


@app.route('/api/create_order/<list:products_list>', methods=["GET"])
@auth.login_required
def create_order(products_list):
    print(request.args.get('operator'))
    if not request.args.get('operator'):
        return jsonify({'error': 'Укажи оператора в query параметре "operator"'})
    products_arr = []
    db.session.commit()
    for prod_id in products_list:
        product = db.session.query(Product).filter(Product.id==prod_id).one()
        product.sell_amount += 1
        db.session.add(product)
        products_arr.append(product)
    db.session.add(Order(products=products_arr, resto_name=restaurant_dict[auth.username()],
                                        operator=request.args.get('operator')))
    db.session.commit()
    return make_response(jsonify({'success': 'Order created'}), 200)


if __name__ == "__main__":
    init_login()
    admin = Admin(app, index_view=MyAdminIndexView(), base_template='my_master.html',
                               name='Панель Администратора', template_mode='bootstrap3', url='/')
    admin.add_view(ProductModelView(Product, db.session, url='/admin/products/', name="Товары"))
    admin.add_view(CategoryModelView(Category, db.session, url='/admin/categories/', name="Категории"))
    admin.add_view(UserModelView(User, db.session, url='/admin/users/', name="Пользователи"))
    admin.add_view(OrderModelView(Order, db.session, url='/admin/orders/', name="Заказы"))
    admin.add_view(StatisticView(url='/admin/statistics/', name="Отчёт"))
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
