from models import *
"""
Здесь происходит создание таблиц и их заполнение из json файлов
"""
db.drop_all()
db.create_all()

for user in User().user_data():
    db.session.add(User(**user))
db.session.commit()

for order in Order().user_data():
    db.session.add(Order(**order))
db.session.commit()

for offer in Offer().user_data():
    db.session.add(Offer(**offer))
db.session.commit()
