from sqlalchemy_mptt.mixins import BaseNestedSets
from settings import app, db
from sqlalchemy.sql import func

class Category(db.Model, BaseNestedSets):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), index=True, unique=True)
    items = db.relationship("Product", backref='item', lazy='dynamic')

    def __repr__(self):
        if self.id is not 1:
            class_elem = self
            def get_name(class_elem):
                if class_elem.id == 1:
                    return 'Базовая категория'
                print(class_elem.name)
                return get_name(class_elem.parent) + ' / ' + str(class_elem.name)
            return get_name(class_elem)
        else:
            return "Базовая категория".format(self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    name = db.Column(db.String(475), index=True)
    cost = db.Column(db.Integer)
    sell_amount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "{}".format(self.name)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('Product', backref='orders', lazy='dynamic')
    created = db.Column(db.DateTime, default=func.now())
    resto_name = db.Column(db.String, default='Не указан')
    money_amount = db.Column(db.Integer)
    product_list = db.Column(db.String)
    operator = db.Column(db.String)


    def __init__(self, resto_name=None, products=None, operator=None):
        self.resto_name = resto_name
        self.products = products
        money_amount = 0
        for product in products:
            money_amount += product.cost
        self.money_amount = money_amount
        self.product_list = ', '.join(str(x) for x in products)
        self.operator = operator


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

if __name__ == "__main__":

    db.session.add(Category(name="Базовая категория"))
    db.session.add_all(
        [
            Category(name="Напитки", parent_id=1),
            Category(name="Алкогольные", parent_id=2),
            Category(name="Безалкогольные", parent_id=2)
        ]
    )
    db.session.add(Product(name="Пиво", category_id=3, cost=100))
    db.session.add(Product(name="Газировка", category_id=4,cost=150))
    db.session.add(User(login="admin", password="admin"))

    db.drop_all()
    db.create_all()
    db.session.commit()
