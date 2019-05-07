from flask import Flask, render_template, session, redirect, url_for, request, g, flash, jsonify, send_from_directory
app = Flask(__name__)
from database import *
from hashlib import sha512
from utils import misc, emails, decorators
from datetime import datetime
from peewee import fn
import requests
import socket
import os
from datetime import datetime
app.secret_key = "mithereicome@91"

import logging
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def make_info_available():

	if "user_id" in session:
		g.user = User.get(User.id == session["user_id"])

@app.context_processor
def just_some_necessary_stuff():
    var = dict()
    if "user_id" in session:
        var["logged_in"] = True
        var["user"] = g.user
    else:
        var["logged_in"] = False

    return var


@app.route('/')
def root():
	if "user_id" in session:
		return redirect(url_for('dashboard'))

	else:
		return render_template('register.html')


@app.route('/send-contact-email/', methods=["POST"])
def sendcontactemail():
	if request.method == "POST":
		name = request.form['name'].strip()
		email = request.form['email'].strip()
		phone = request.form['phone'].strip()
		regard = request.form['regard'].strip()
		query = request.form['query'].strip()
	try:
		emails.send_query_email(name,email,phone,regard,query)
		flash("Your Query has been sent!")
		return redirect(url_for("root"))
	except:
		flash("There was an error in sending the email")
		return redirect(url_for("root"))

@app.route('/register/', methods=["GET", "POST"] )
def register():
	if request.method == "GET":
		return render_template('register.html')

	elif request.method == "POST":
		name = request.form['name'].strip()
		email = request.form['email'].strip()
		password = request.form['password'].strip()
		profilepicture = "http://lorempixel.com/200/200/"
		bio = "You can change this below!! "
		key = misc.generate_confirmation_key()

		if not name:
			flash("Please enter a name smarty!")
			return render_template("register.html")

		if not email:
			flash("A valid email id would be appreciated!")
			return render_template("register.html")

		if not password or len(password) < 8:
			flash("Please select a password more than 8 characters!")
			return render_template("register.html")

		try:

			user = User.get(User.email == email)
			flash("A user with this email id already exsists please login using your credentials")
			return redirect(url_for('login'))

		except User.DoesNotExist:

			try:
				try:
					maxid=User.select()[-1].id
				except:
					maxid=0
				user = User.create(id =int(maxid)+1,name=name , email=email , password = sha512(password).hexdigest() ,bio=bio, conf_key = key , emailconf = False,picturefilename=profilepicture)
				emails.send_confirmation_email(email, name , key)
				session['user_id'] = user.id
				flash("Ahoy! You're registered!")
				return redirect(url_for('dashboard'))

			except:

				return "There was an error in the system <br> Please contact the administrator with the details of the problem at rajattomar1301@gmail.com"

@app.route('/login/', methods=["GET", "POST"])
def login():
	if "user_id" in session:
		return redirect(url_for('dashboard'))

	if request.method == "GET":
		return render_template("login.html")

	elif request.method == "POST":
		user_email = request.form['email'].strip()
		password = request.form['password'].strip()
		try:
	 		user = User.get(User.email == str(user_email) )
	 		if user.password == sha512(password).hexdigest():
	 			flash("Ahoy you're in eh!")
	 			session["user_id"] = user.id
	 			return redirect(url_for('dashboard'))
	 		else:
	 			flash("Wrong Password there buddy!")
	 			return render_template("login.html")
		except:
	 		flash("User not found buddy!")
	 		return render_template("login.html")


@app.route('/dashboard/', methods=["GET"])
@decorators.login_required
def dashboard():
	if request.method == "GET":
		return render_template('dashboard.html',User=g.user)

@app.route('/update-details/', methods=["POST"])
@decorators.login_required
def update_details():
	name = request.form['name'].strip()
	email = request.form['email'].strip()
	bio = request.form['bio'].strip()

	if email != "" and emails.is_valid_email(email) and g.user.email != email :
		g.user.email = email
		g.user.emailconf = False
		confkey = misc.generate_confirmation_key()
		g.user.conf_key = confkey
		emails.send_confirmation_email(g.user.email, g.user.name, confkey)
		g.user.save()
		flash("Email changed!")
	if name != "" and g.user.name != name:
		g.user.name=name
		g.user.emailconf = False
		confkey = misc.generate_confirmation_key()
		g.user.conf_key = confkey
		emails.send_confirmation_email(g.user.email, g.user.name, confkey)
		g.user.save()
		flash("Name changed!")
	if bio != "" and g.user.bio != bio:
		g.user.bio=bio
		g.user.emailconf = False
		confkey = misc.generate_confirmation_key()
		g.user.conf_key = confkey
		emails.send_confirmation_email(g.user.email, g.user.name, confkey)
		g.user.save()
		flash("bio changed!")

	return redirect(url_for('dashboard'))


@app.route('/confirm_email_link/<confirmation_key>/', methods=["GET"])
@decorators.login_required
def confirm_email_link(confirmation_key):
    if confirmation_key == g.user.conf_key:
        flash("Email confirmed!")
        g.user.emailconf = True
        g.user.save()
    else:
        flash("Email Not Verified.")
    return redirect(url_for('dashboard'))

@app.route('/product_creation/', methods=["GET", "POST"])
@decorators.login_required
def product_creation():
	if request.method == "GET":
		return render_template("product_creation.html")

	elif request.method == "POST":
		
		name = request.form['name'].strip()
	
		description = request.form['description'].strip()
	
		#file = request.files['file']
		deadline = request.form['deadline'].strip()

		#meantfor = request.form['meantfor'].strip()
		'''subject = request.form['subject'].strip()
		'''
		filename = request.form['picturefilename'].strip()
	
		author = g.user.name
		minbid=request.form['minbid'].strip()
	
		
		#meantforsection = request.form['meantforsection'].strip()

		try:
			maxid=Product.select()[-1].id
		except:
			maxid=0
	
		#HomeWork.create(name = name , description = description, filename= filename, originalname = file.filename, deadline = deadline, teacher = g.user.id, meantfor = meantfor,meantforsection = meantforsection ,subject = subject, teachername = author)
		Product.create(id=int(maxid)+1,name = name , description = description,picturefilename= filename,user = author, minbid=int(minbid), deadline = deadline )
		#file.save(os.path.join(os.getcwd(),"attachments/"+ filename))
		flash("Project successfully created!")
		return redirect(url_for('dashboard'))



@app.route('/products/<id>',methods=["GET","POST"])
@decorators.login_required
def product_details(id):
	if request.method=="GET":
	
		products=Product.select()
		bids=Bids.select()
		#user = User.get(User.id == Bids.user)
		user=Bids.user
		users=User.select()
		
		maxbid={}	
		for bid in bids:
			if bid.product==id:
				for usr in users:
					if usr.id==bid.user:
		
						name=usr.name
				if name in list(maxbid.keys()):
					if int(bid.bidamount)>maxbid[name]:
						maxbid[name]=int(bid.bidamount)
				else:
					maxbid[name]=int(bid.bidamount)

		if maxbid!={}:
			maximum=[list(maxbid.keys())[0],maxbid[list(maxbid.keys())[0]]]
			for i in list(maxbid.keys()):
				if maxbid[i]>maximum[1]:
					maximum=[i,maxbid[i]]

		else:
			maximum=[0,"none"]

		for product in products:
		
			if product.id==id:
				date=str(product.deadline)
	
				date=date.split()
	
				deadline=datetime.strptime(date[0]+" "+date[1],"%Y-%m-%d %H:%M")
				present=datetime.now()
				if present>=deadline:
					status=True
				else:
					status=False
	
				return render_template('product.html',Product=product,Bids=maxbid,User=g.user,closed=status,Winnerbid=maximum[1],Winnername=maximum[0])

	if request.method=="POST":

		bid=request.form['bid'].strip()
	
		products=Product.select()
		for product in products:
		
			if product.id==id:
		
				if int(product.minbid)>int(bid):
					return redirect(url_for('products'))
				else:
					try:
						maxid=Bids.select()[-1].id
					except:
						maxid=0
	
					Bids.create(id=int(maxid)+1,user=g.user.id,product=id,bidamount=int(bid))
		
					flash("Bid placed")
					return redirect(url_for('products'))



		try:
			maxid=Bids.select()[-1].id
		except:
			maxid=1

		Bids.create(id=int(maxid)+1,user=g.user.id,product=id,bidamount=int(bid))

		flash("Bid placed")
		return redirect(url_for('products'))


@app.route('/products/',methods=["GET"])
@decorators.login_required
def products():
	products=Product.select()
	bids=Bids.select()
	maxbid={}	
	for bid in bids:
		if bid.product in list(maxbid.keys()):
			if int(bid.bidamount)>maxbid[bid.product]:
				maxbid[bid.product]=int(bid.bidamount)
		else:
			maxbid[bid.product]=int(bid.bidamount)

	
		

	return render_template('product_display.html',Products=products,maxbid=maxbid)	

@app.route('/logout/')
def logout():
	session.clear()
	flash("Logout successfully captain!")
	return redirect(url_for('login'))

@app.route('/reset-password/', methods=["GET", "POST"])
def reset_password():
	if "user_id" in session:
		flash("You are already logged in!")
		return redirect(url_for('dashboard'))
	if request.method == "GET":
		return render_template('reset_password.html')

	elif request.method == "POST":
		email = request.form['email'].strip()

	try:
		user = User.get(User.email == email)
		conf_key = misc.generate_confirmation_key()
		user.conf_key = conf_key
		emails.send_reset_email(user.email,user.name, user.conf_key)
		user.save()
		flash("An email with the instructions has been sent to your mail id!")
		return redirect(url_for('reset_password'))

	except User.DoesNotExist:
		flash("No account associated with this email address!")
		return redirect(url_for('reset_password'))

@app.route('/reset-password-page/<email>/<key>/', methods=["GET","POST"])
def reset_password_page(email,key):
	if "user_id" in session:
		flash("You are already logged in!")
		return redirect(url_for('dashboard'))
	if request.method == "GET":
		try:
			user = User.get(User.email == email)
			if user.conf_key == key:
				return render_template("reset_password_set.html", email = user.email , key = key)
			else:
				return "You are using an invalid key"

		except User.DoesNotExist:
			return "Your are using an invalid link!"

	elif request.method == "POST":
		try:
			user = User.get(User.email == email)
			password = request.form['password'].strip()
			if user.conf_key == key:
				user.password = sha512(password).hexdigest()
				user.conf_key = "null"
				user.save()
				flash("Your password has been changed!")
				return redirect(url_for('login'))
			else:
				return "Don't try to fool me!"
		except User.DoesNotExist:
			return "haha! you can't fool me you hacker!"






@app.before_request
def before_request():
	try:
	    db.connect()
	except OperationalError:
	    db.close()
	    db.connect()

@app.teardown_request
def teardown_request(exc):
    db.close()

def allowed_files(name):
	exts = ['.jpg', '.jpeg', '.png']
	for i in exts:
		if name.endswith(i):
			return True
	return False

def generate_name(name):
	if name.endswith('.jpeg'):
		ext = name[len(name)-5::]
	else:
		ext = name[len(name)-4::]
	name = name.strip(ext)
	name += "_"+misc.generate_random_string(32)
	name += ext
	return name


if __name__ == "__main__":
	app.run(ssl_context=('cert.pem', 'key.pem'))
