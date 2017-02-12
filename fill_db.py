from models import Product, Category, User, Order
from settings import db
import random

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
    db.session.add(Product(name="Вода", category_id=4,cost=150))
    db.session.add(User(login="admin", password="admin"))

    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.close()
