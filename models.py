from app import db
import json
import datetime

"""
Создаем таблицы
"""

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100), unique=True)

    def user_data(self):
        with open("data/Users.json", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def obj_to_dict(self, obj):
        """Преобразуем объект класса в словарь"""
        return {
            "id": obj.id,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "age": obj.age,
            "email": obj.email,
            "role": obj.role,
            "phone": obj.phone
        }


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = db.relationship("User", foreign_keys="Order.customer_id")
    executor = db.relationship("User", foreign_keys="Order.executor_id")

    def user_data(self):
        with open("data/Orders.json", encoding="utf-8") as file:
            data = json.load(file)
            for i in data:
                if i["start_date"]:  # преобразуем строчный формат даты в питоновский
                    month, day, year = [int(x) for x in i["start_date"].split("/")]
                    i["start_date"] = datetime.date(year, month, day)
                if i["end_date"]:
                    month, day, year = [int(x) for x in i["end_date"].split("/")]
                    i["end_date"] = datetime.date(year, month, day)
            return data

    def obj_to_dict(self, obj):
        return {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "start_date": obj.start_date,
            "end_date": obj.end_date,
            "address": obj.address,
            "price": obj.price,
            "customer_id": obj.customer_id,
            "executor_id": obj.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order = db.relationship("Order")
    executor = db.relationship("User")

    def user_data(self):
        with open("data/Offers.json", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def obj_to_dict(self, obj):
        return {
            "id": obj.id,
            "order_id": obj.order_id,
            "executor_id": obj.executor_id
        }
