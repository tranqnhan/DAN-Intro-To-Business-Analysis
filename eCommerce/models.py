from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    address = db.Column(db.String(150))
    credits = db.Column(db.Float)

class CartItem(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    qty_ordered = db.Column(db.Integer)

class OrderItem(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)

    qty_ordered = db.Column(db.Integer)
    name = db.Column(db.String(100))  # In case the item is deleted, this is for order history
    cost = db.Column(db.Float)

    item = db.relationship('Item', backref=db.backref('orders'))
    order = db.relationship('Order', backref=db.backref('items'))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    itemname = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    imageurl = db.Column(db.String(1000))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shipaddress = db.Column(db.String(150))