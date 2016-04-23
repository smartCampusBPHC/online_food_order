from ancapp import app
from flask import Flask, render_template, url_for, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
#n= no of food items available
from modules import User ,FoodItem ,Order ,OrderItem 
#defining the static variables 
n=200
price_of_parcel=5
#defining the total price after parcel
total_price_after_parcel=0
#defining the total price before parcel
total_price_before_parcel=0
#defines the dictionaries
food_quant[n]
dict_for_order_page[n]
dict_for_checkout_page[n]
Dict_for_parcel[n]



@app.route("/")
def hello():
    return "Hello World!"


#**********************************************************************************************************************************************************************************************************#


@app.route("/login")
def index():
    pass


#************************************************************************************************************************************************************************************************************#


@app.route("/main",methods=['GET','POST'])
def main():
	if request.method=='GET':
		render_template('index.html')
	else:
		for i in range(n):
			#query name
			sql_name=text('select name from FoodItem where id=%d',i)
			name=db.engine.execute(sql_name)
			#QUERY image
			sql_image=text('select image from FoodItem where id=%d',i)
			image=db.engine.execute(sql_image)
			#query price
			sql_price=text('select price from FoodItem where id=%d',i)
			price=db.engine.execute(sql_price)
			#query availablilty
			sql_avail=text('select availability from FoodItem where id=%d',i)
			avail=db.engine.execute(sql_avail)
			#query discription
			sql_dis=text('select description from FoodItem where id=%d',i)
			dis=db.engine.execute(sql_dis)
			#query veg
			sql_veg=text('select cat from FoodItem where id=%d',i)
			veg=db.engine.execute(sql_veg)
			sql_cat=text('select cat from FoodItem where id=%d',i)
			cat=db.engine.execute(sql_cat)
			dict_for_order_page[i]=tuple(i,name,price,image,avail,dis,veg,cat)
		render_template('product.html',params=dict_for_order_page)

#***************************************************************************************************************************************************************************#

@app.route("/orders" ,methods=['GET','POST'])
def order():
	if request.method=='GET':
		for i in range(n):
			#query name
			sql_name=text('select name from FoodItem where id=%d',i)
			name=db.engine.execute(sql_name)
			#QUERY image
			sql_image=text('select image from FoodItem where id=%d',i)
			image=db.engine.execute(sql_image)
			#query price
			sql_price=text('select price from FoodItem where id=%d',i)
			price=db.engine.execute(sql_price)
			#query availablilty
			sql_avail=text('select availability from FoodItem where id=%d',i)
			avail=db.engine.execute(sql_avail)
			#query discription
			sql_dis=text('select description from FoodItem where id=%d',i)
			dis=db.engine.execute(sql_dis)
			#query veg
			sql_veg=text('select cat from FoodItem where id=%d',i)
			veg=db.engine.execute(sql_veg)
			#query category
			sql_cat=text('select cat from FoodItem where id=%d',i)
			cat=db.engine.execute(sql_cat)
			#add to the tuple that is send to the front  end
			dict_for_order_page[i]=tuple(i,name,price,image,avail,dis,veg,cat)
		render_template('product.html', params=dict_for_order_page)
	else:
		for i in range(n):
			quant=request.form[str(i)]
			food_quant[i]=((int)quant)
		for i in range(n):
			if food_quant[i]==0:
				pass
			else:
				quant=food_quant[i]
				#query the name of the food item and store it in name
				sql_name=text('select name from FoodItem where id=%d',i)
				name=db.engine.execute(sql_name)
				#query of price for that food stored in variable price_of_food
				sql_price=text('select price from FoodItem where id=%d',i)
				price_of_food=db.engine.execute(sql_price)
				#per food item the total cost is stored in total price per food item
				total_price_per_food_item=(quant*price_of_food)
				#total price before parcel
				total_price_before_parcel=total_price+total_price_per_food_item
				#each tuple we create we send these particular values to the front end 
				dict_for_checkout_page[i]=tuple(name,quant,price_of_food,total_price_per_food_item,orderid,studentname)
				#insert in order table
				sql_order=text('insert into order values(%d,%s,%s)',x,studentname,total_price)
				db.engine.execute(sql_order)
				#insert in orderitem
				sql_orderitem=text('insert into OrderItem values(%d,%d,%d)',x,i,quant)
				db.engine.execute(sql_)
				Dict_for_parcel[i]=tuple(i,name,quant)
		#setting condition on total price of food after parcel
		total_price_after_parcel=total_price_before_parcel
		#render the page
		render_template('parcel.html',params=Dict_for_parcel)




#*********************************************************************************************************************************************************************************#						



@app.route('/parcel',methods=['GET','POST'])
def parcel:
	if request.method='GET':		
		render_template('parcel.html',params=z)
	#once the submit button is pressed a post request is sent
	else:
		for i in range(n):
			if quant==0:
				pass
			else:
				quant_parcel=request.form['quant']
				price_of_parcel[i]=parcel_price*quant_parcel
				total_price_after_parcel=total_price_after_parcel+price_of_parcel[i]
		#render the page
		render_template('checkout_edited.html',params=dict_for_checkout_page,params1=total_price_before_parcel,params2=total_price_after_parcel,params3=price_of_parcel)




#***********************************************************************************************************************************************************************************#



@app.route('/contact',methods=['GET','POST'])
def contact():
	if request.method=='GET':
		render_template('contact.html')
	else:
		username=request.form['username']
		email=request.form['useremail']
		phone=request.form['userphone']
		msg=request.form['usermsg']
		#add to table contact
		sql_contact=text('insert into contact values (%s,%s,%s,%s)',username,email,phone,msg)
		db.engine.execute(sql_contact)
		render_template('thankyou.html')


#*******************************************************************************************************************************************************************************************#






