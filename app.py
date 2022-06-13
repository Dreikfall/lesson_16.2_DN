from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import *
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


@app.route("/users", methods=["GET", "POST"])
def get_all_users():
    if request.method == "POST":
        data = request.json
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.obj_to_dict(user))

    users = User.query.all()
    users_list = []
    for i in users:
        users_list.append(i.obj_to_dict(i))
    return jsonify(users_list)


@app.route("/users/<int:sid>", methods=["GET", "PUT", "DELETE"])
def get_id_user(sid):
    if request.method == "PUT":
        data = request.json
        db.session.query(User).filter(User.id == sid).update(data)
        db.session.commit()
        user = User.query.get(sid)
        return jsonify(user.obj_to_dict(user))

    if request.method == "DELETE":
        db.session.query(User).filter(User.id == sid).delete()
        db.session.commit()
        return f"User id={sid} delete"

    user = db.session.query(User).get(sid)
    return jsonify(user.obj_to_dict(user))


@app.route("/orders", methods=["GET", "POST"])
def get_all_orders():
    """В POST происходит преобразование строчного формата даты в питоновский"""
    if request.method == "POST":
        data = request.json
        time_1 = [int(i) for i in data['start_date'].split("/")]
        time_2 = [int(i) for i in data['end_date'].split("/")]
        order = Order(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            start_date=datetime.date(time_1[0], time_1[1], time_1[2]),
            end_date=datetime.date(time_2[0], time_2[1], time_2[2]),
            address=data.get('address'),
            price=data.get('price'),
            customer_id=data.get('customer_id'),
            executor_id=data.get('executor_id')
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(order.obj_to_dict(order))
    orders = Order.query.all()
    orders_list = []
    for i in orders:
        orders_list.append(i.obj_to_dict(i))
    return jsonify(orders_list)


@app.route("/orders/<int:oid>", methods=["GET", "PUT", "DELETE"])
def get_id_order(oid):
    if request.method == "PUT":
        data = request.json
        db.session.query(Order).filter(Order.id == oid).update(data)
        db.session.commit()
        order = Order.query.get(oid)
        return jsonify(order.obj_to_dict(order))

    if request.method == "DELETE":
        db.session.query(Order).filter(Order.id == oid).delete()
        db.session.commit()
        return f"Order id={oid} delete"

    order = db.session.query(Order).get(oid)
    return jsonify(order.obj_to_dict(order))


@app.route("/offers", methods=["GET", "POST"])
def get_all_offers():
    if request.method == "POST":
        data = request.json
        offer = Offer(**data)
        db.session.add(offer)
        db.session.commit()
        return jsonify(offer.obj_to_dict(offer))
    orders = Offer.query.all()
    offers_list = []
    for i in orders:
        offers_list.append(i.obj_to_dict(i))
    return jsonify(offers_list)


@app.route("/offers/<int:oid>", methods=["GET", "PUT", "DELETE"])
def get_id_offer(oid):
    if request.method == "PUT":
        data = request.json
        db.session.query(Offer).filter(Offer.id == oid).update(data)
        db.session.commit()
        offer = Offer.query.get(oid)
        return jsonify(offer.obj_to_dict(offer))

    if request.method == "DELETE":
        db.session.query(Offer).filter(Offer.id == oid).delete()
        db.session.commit()
        return f"Offer id={oid} delete"

    offer = db.session.query(Offer).get(oid)
    return jsonify(offer.obj_to_dict(offer))


if __name__ == "__main__":
    app.run(debug=True)
