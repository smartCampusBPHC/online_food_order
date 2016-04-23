from ancapp import db
from ancapp import app
import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow() \
                                          + datetime.timedelta(hours=5.5))
    name = db.Column(db.String)
    phone = db.Column(db.BigInteger, unique=True)
    email = db.Column(db.String, unique=True)
    def __repr__(self):
        return "Id: {} {}".format(self.id,self.name)

class FoodItem(db.Model):
    __tablename__ = "fooditem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    availability = db.Column(db.Boolean, default=True)
    image = db.Column(db.String, unique=True)
    def __repr__(self):
        return "Id: {} {}".format(self.id,self.name)
     
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_ordered = db.Column(db.DateTime, default=datetime.datetime.utcnow() \
                                          + datetime.timedelta(hours=5.5))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='orders')
    amount = db.Column(db.Integer)
    def __repr__(self):
        return "Id: {} {} Amt: Rs.{}".format(self.id,self.user.name,self.amount)
    
class OrderItem(db.Model):
    __tablename__ = "orderitem"
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', backref='orderitems')
    fooditem_id = db.Column(db.Integer, db.ForeignKey('fooditem.id'))
    fooditem = db.relationship('FoodItem', backref='orderitems')
    quantity = db.Column(db.Integer)
    def __repr__(self):
        return "Id: {} Order Id: {} {} Qty: {}".format(self.id, self.order_id,
                                                       self.fooditem.name, self.quantity)
