from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, helpers, expose
from models import Product
from flask import Flask, url_for, redirect, request
from forms import LoginForm, RegistrationForm
from settings import app, db
import flask_login as login
import flask_admin as admin


class StatisticView(BaseView):

    @expose('/')
    def statistic(self):
        products = Product.query.all()
        sorted_products = list(sorted(products, key= lambda x: -x.sell_amount))
        for product in sorted_products:
            product.profit = product.cost*product.sell_amount
        return self.render('statistic_template.html',products=sorted_products)


class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


class ProductModelView(MyModelView):
    column_list = ('name', 'cost', 'item', 'id')
    form_create_rules = ('name', 'cost', 'item')
    column_labels = dict(name='Название', cost='Стоимость, руб', item='Категория')


class CategoryModelView(MyModelView):
    column_list = ('name', 'parent', 'id')
    form_create_rules = ('name', 'parent')
    column_labels = dict(name='Название', parent='Категория')


class UserModelView(MyModelView):
    column_list = ('login', 'email', 'password')
    form_create_rules = ('login', 'email', 'password')
    column_labels = dict(login='Логин',password='Пароль')


class OrderModelView(MyModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_list = ('id', 'money_amount', 'resto_name', 'product_list', 'operator', 'created')
    column_labels = dict(money_amount='Стоимость заказа, руб', resto_name='Название ресторана',
                                       product_list='Список заказа',operator='Оператор', created='Дата создания')


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
