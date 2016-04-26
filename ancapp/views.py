from ancapp import app, db
from flask import Flask, render_template, url_for,jsonify, request, redirect, session, g
from flask_oauthlib.client import OAuth
from .models import User,Category, FoodItem, OrderItem, Order
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required
import razorpay
import json

###defining the static variables 
##n=200
##price_of_parcel=5
###defining the total price after parcel
##total_price_after_parcel=0
###defining the total price before parcel
##total_price_before_parcel=0
###defines the dictionaries
##food_quant={}
##dict_for_order_page={}
##dict_for_checkout_page={}
##Dict_for_parcel={}

lm =  LoginManager()
lm.init_app(app)
lm.login_view = 'login'
razor = razorpay.Client(auth=(app.config.get('RAZOR_KEY'), app.config.get('RAZOR_SECRET')))
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    if current_user is None or not current_user.is_authenticated:
        return google.authorize(callback=url_for('authorized', _external=True))
    return redirect(url_for('main'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user = User.query.filter_by(google_id = me.data['id']).first()
    if not user:
        user = User()
        user.google_id = me.data['id']
        user.name = me.data['name']
        user.email =  me.data['email']
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('main'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/product', methods=['GET','POST'])
# @login_required
def main():
    if request.method == 'GET':
        categories = Category.query.all() 
        return render_template('product.html',categories = categories)

    if request.method=='POST':
        current_user =  User.query.get(1)
        order = Order()
        order.user = current_user
        db.session.add(order)
        quantity = {}
        foodItems = FoodItem.query.all()
        total = 0
        for food in foodItems:
            qty = int(request.form[str(food.id)])
            if  qty > 0:
                quantity[food] = (qty , qty * food.price)
                total += quantity[food][1]
                orderitem =  OrderItem()
                orderitem.order = order
                orderitem.fooditem = food
                orderitem.quantity = qty
                db.session.add(orderitem)

        order.amount = total
        db.session.commit()
        return redirect( url_for('checkout', orderId = order.id) )


@app.route('/checkout/<int:orderId>/',methods=['GET','POST'])
# @login_required
def checkout(orderId):
    if request.method=='GET':
        order = Order.query.get(orderId)
        current_user =  User.query.get(1)
        return render_template('checkout_edited.html',current_user = current_user, order = order)

@app.route('/process_order', methods=['POST'])
# @login_required
def process_order():
    if request.method == 'POST':
        razorId = request.form['razorpay_payment_id']
        orderId = int(request.form['order_id'])
        order = Order.query.get(orderId)
        razorJSON = razor.payment.fetch(razorId)
        print razorJSON
        if razorJSON['amount'] == order.amount *100:
            return "Your payment is successful"
        else:
            return "Payment not succesful"
    
        

##@app.route("/main")
##def main():
##	render_template('index.html')

##
###***************************************************************************************************************************************************************************#
##
##@app.route("/orders" ,methods=['GET','POST'])
##def order():
##	if request.method=='GET':
##		for i in range(n):
##			#query name
##			sql_name=text('select name from FoodItem where id=%d',i)
##			name=db.engine.execute(sql_name)
##			#QUERY image
##			sql_image=text('select image from FoodItem where id=%d',i)
##			image=db.engine.execute(sql_image)
##			#query price
##			sql_price=text('select price from FoodItem where id=%d',i)
##			price=db.engine.execute(sql_price)
##			#query availablilty
##			sql_avail=text('select availability from FoodItem where id=%d',i)
##			avail=db.engine.execute(sql_avail)
##			#query discription
##			sql_dis=text('select description from FoodItem where id=%d',i)
##			dis=db.engine.execute(sql_dis)
##			#query veg
##			sql_veg=text('select cat from FoodItem where id=%d',i)
##			veg=db.engine.execute(sql_veg)
##			#query category
##			sql_cat=text('select cat from FoodItem where id=%d',i)
##			cat=db.engine.execute(sql_cat)
##			#add to the tuple that is send to the front  end
##			dict_for_order_page[i]=tuple(i,name,price,image,avail,dis,veg,cat)
##		render_template('product.html', params=dict_for_order_page)
##	else:
##		for i in range(n):
##			quant=request.form[str(i)]
##			food_quant[i]=((int)quant)
##		for i in range(n):
##			if food_quant[i]==0:
##				pass
##			else:
##				quant=food_quant[i]
##				#query the name of the food item and store it in name
##				sql_name=text('select name from FoodItem where id=%d',i)
##				name=db.engine.execute(sql_name)
##				#query of price for that food stored in variable price_of_food
##				sql_price=text('select price from FoodItem where id=%d',i)
##				price_of_food=db.engine.execute(sql_price)
##				#per food item the total cost is stored in total price per food item
##				total_price_per_food_item=(quant*price_of_food)
##				#total price before parcel
##				total_price_before_parcel=total_price+total_price_per_food_item
##				#each tuple we create we send these particular values to the front end 
##				dict_for_checkout_page[i]=tuple(name,quant,price_of_food,total_price_per_food_item,orderid,studentname)
##				#insert in order table
##				sql_order=text('insert into order values(%d,%s,%s)',x,studentname,total_price)
##				db.engine.execute(sql_order)
##				#insert in orderitem
##				sql_orderitem=text('insert into OrderItem values(%d,%d,%d)',x,i,quant)
##				db.engine.execute(sql_)
##				Dict_for_parcel[i]=tuple(i,name,quant)
##		#setting condition on total price of food after parcel
##		total_price_after_parcel=total_price_before_parcel
##		#render the page
##		render_template('parcel.html',params=Dict_for_parcel)
##
##
##
##
###*********************************************************************************************************************************************************************************#						
##
##
##
##@app.route('/parcel',methods=['GET','POST'])
##def parcel:
##	if request.method='GET':		
##		render_template('parcel.html',params=z)
##	#once the submit button is pressed a post request is sent
##	else:
##		for i in range(n):
##			if quant==0:
##				pass
##			else:
##				quant_parcel=request.form['quant']
##				price_of_parcel[i]=parcel_price*quant_parcel
##				total_price_after_parcel=total_price_after_parcel+price_of_parcel[i]
##		#render the page
##		render_template('checkout_edited.html',params=dict_for_checkout_page,params1=total_price_before_parcel,params2=total_price_after_parcel,params3=price_of_parcel)
##
##
##
##
###***********************************************************************************************************************************************************************************#
##
##
##
##@app.route('/contact',methods=['GET','POST'])
##def contact():
##	if request.method=='GET':
##		render_template('contact.html')
##	else:
##		username=request.form['username']
##		email=request.form['useremail']
##		phone=request.form['userphone']
##		msg=request.form['usermsg']
##		#add to table contact
##		sql_contact=text('insert into contact values (%s,%s,%s,%s)',username,email,phone,msg)
##		db.engine.execute(sql_contact)
##		render_template('thankyou.html')
##
##
###*******************************************************************************************************************************************************************************************#
##
##
