from flask_admin.contrib.sqla import ModelView
from ancapp import db, admin
from ancapp.models import User, FoodItem, Order, OrderItem

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(FoodItem, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderItem, db.session))
