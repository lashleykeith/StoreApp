# Item Catalog Application Project
from flask import (Flask, render_template, request, redirect, jsonify,
                   url_for, flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Store, InventoryItem, User

# Import Login session
from flask import session as login_session
import random
import string

# Imports for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

# Import login decorator
from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(
     open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Store Inventory Application"

engine = create_engine('sqlite:///storeinventorywithusers.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

# Create a state token to request forgery and
# store it in the session for later validation




def login_required(l):
	@wraps(l)
	def decorated_function(*arg, **kwarg):
		if 'username' not in login_session:
			return redirect('/login')
		return l(*arg, **kwarg)
	return decorated_function


@app.route('/login')
def showlogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application-json'
		return response

	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code in credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps(
			'Failed to upgrade the authorization code'), 401)
		response.headers['Content-Type'] = 'application-json'
		return response

	# Check that the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
	# If there was an error in the access token info, abort
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	# Access token within the app
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps(
			'Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use

	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id
	response = make_response(json.dumps('Successfully connected users', 200))

    # Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()
	login_session['provider'] = 'google'
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# See if user exists or if it doesn't make a new one
	print 'User email is' + str(login_session['email'])
	user_id = getUserID(login_session['email'])
	if user_id:
		print 'Existing user#' + str(user_id) + 'matches this email'
	else:
		user_id = createUser(login_session)
		print 'New user id#' + str(user_id) + 'created'
	login_session['user_id'] = user_id
	print 'Login session is tied to :id#' + str(login_session['user_id'])

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius:150px;- \
		webkit-border-radius:150px;-moz-border-radius: 150px;">'
	flash("You are now logged in as %s" % login_session['username'])
	print "Done!"
	return output


# User Helper Functions
def createUser(login_session):
	newUser = User(name=login_session['username'],
					email=login_session['email'],
					picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).first()
	return user.id


def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).first()
	return user


def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).first()
		return user.id
	except:
		return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected User
	access_token = login_session.get('access_token')
	print 'In gdisconnect access token is %s', access_token
	print 'User name is: '
	print login_session['username']
	if access_token is None:
		print 'Access Token is None'
		response = make_response(json.dumps('Current user not connected'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url,'GET')[0]
	print 'result is'
	print result
	if result['status'] == '200':
		response = make_response(json.dumps('Successfully disconnect.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for \
								given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/logout')
def logout():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
				gdisconnect()
				del login_session['gplus_id']
				del login_session['access_token']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		flash("You have successfully been logged out")
		return redirect(url_for('showStores'))
	else:
		flash("You were not logged in")
		return redirect(url_for('showStores'))

# JSON APIs to view Store Information
@app.route('/store/<int:store_id>/inventory/JSON')
def storeInventoryJSON(store_id):
	store = session.query(Store).filter_by(id=store_id).one()
	items = session.query(InventoryItem).filter_by(
							store_id=store_id).all()
	return jsonify(InventoryItems=[i.serialize for i in items])

@app.route('/store/<int:store_id>/inventory/<int:inventory_id>/JSON')
def inventoryItemJSON(store_id, inventory_id):
	Inventory_Item = session.query(InventoryItem).filter_by(id=inventory_id).one()
	return jsonify(Inventory_Item=Inventory_Item.serialize)

@app.route('/store/JSON')
def storeJSON():
	stores = session.query(Store).all()
	return  jsonify(stores=[r.serialize for r in stores])

# Show all stores
@app.route('/')
@app.route('/store/')
def showStores():
	stores = session.query(Store).order_by(asc(Store.name))
	if 'username' not in login_session:
		return render_template('publicstores.html',
								stores=stores)
	else:
		return render_template('stores.html', stores=stores)

# Create a new store
@app.route('/store/new/', methods=['GET','POST'])
@login_required
def newStore():
	if request.method == 'POST':
		newStore = Store(name=request.form['name'],
							user_id=login_session['user_id'])
		session.add(newStore)
		flash('New Store %s Successfully Created' % newStore.name)
		session.commit()
		return redirect(url_for('showStores'))
	else:
		return render_template('newStore.html')

#Edit a store
@app.route('/store/<int:store_id>/edit/', methods=['GET','POST'])
@login_required
def editStore(store_id):
	editedStore = session.query(Store).filter_by(
								id=store_id).one()
	if editedStore.user_id != login_session['user_id']:
		return "<script>function myFunction(){alert('You are not authorized to \
                edit this store. Please create your own store \
                in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			editedStore.name = request.form['name']
			session.add(editedStore)
			session.commit()
			flash('Store Successfully Edited %s'
				% editedStore.name)
			return redirect(url_for('showStores'))
	else:
		return render_template('editStore.html',
								store=editedStore)

# Delete a store
@app.route('/store/<int:store_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteStore(store_id):
	storeToDelete = session.query(Store).filter_by(
									id=store_id).one()
	if storeToDelete.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('you are not authorized to \
		delete this store. Please create your own store \
		to delete');}</script><body onLoad = 'myFunction()''>"
	if request.method == 'POST':
		session.delete(storeToDelete)
		flash('%s Successfully Deleted' % storeToDelete.name)
		session.commit()
		return redirect(url_for('showStores',
						store_id=store_id))
	else:
		return render_template('deleteStore.html',
								store=storeToDelete)

# Show a store inventory
@app.route('/store/<int:store_id>/')
@app.route('/store/<int:store_id>/inventory/')
def showInventory(store_id):
	store = session.query(Store).filter_by(id=store_id).first()
	creator = getUserInfo(store.user_id)
	items = session.query(InventoryItem).filter_by(
							store_id=store_id).all()

	if 'username' not in login_session:
		return render_template('publicinventory.html', items=items,
								store=store, creator=creator)
	else:
		return render_template('inventory.html',items=items,
								store=store, creator=creator)

# Create a new inventory item
@app.route('/store/<int:store_id>/inventory/new/',
			methods=['GET', 'POST'])
@login_required
def newInventoryItem(store_id):
	store = session.query(Store).filter_by(id=store_id).one()
	if request.method == 'POST':
		newItem = InventoryItem(name=request.form['name'],
								description=request.form['description'],
								price=request.form['price'],
								course=request.form['course'],
								store_id=store_id,
								user_id=store.user_id)
		session.add(newItem)
		session.commit()
		flash('New Inventory %s Item Successfully Created' % (newItem.name))
		return redirect(url_for('showInventory', store_id=store_id))
	else:
		return render_template('newinventoryitem.html', store_id=store_id)

# Edit a inventory item
@app.route('/store/<int:store_id>/inventory/<int:inventory_id>/edit', 
			methods=['GET','POST'])
@login_required
def editInventoryItem(store_id, inventory_id):
	editedItem = session.query(InventoryItem).filter_by(id=inventory_id).one_or_none()
	store = session.query(Store).filter_by(id=store_id).one()
	if login_session['user_id'] != store.user_id:
		return "<script>function myFunction() {alert('You are not authorized to \
		edit inventory items to this store. Please create your own \
		store in order to edit items.\
		');}</script><body onload='myFunction()''>"

	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash('Inventory Item Successfully Edited')
		return redirect(url_for('showInventory', store_id=store_id))
	else:
		return render_template('editinventoryitem.html',
								store_id=store_id,
								inventory_id=inventory_id, item=editedItem)

 # Delete a inventory item
@app.route('/store/<int:store_id>/inventory/<int:inventory_id>/delete',
 			methods=['GET','POST'])
@login_required
def deleteInventoryItem(store_id, inventory_id):
	store = session.query(Store).filter_by(id=store_id).one()
	itemToDelete = session.query(InventoryItem).filter_by(id=inventory_id).one()
	if login_session['user_id'] != store.user_id:
		return "<script>function myFunction() {alert ('you are not authorized to \
		delete inventory items to this store. Please create your own \
		store in order to delete items\
		');}</script><body onload='myFunction()''>"	
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('Inventory Item Successfully Deleted')
		return redirect(url_for('showInventory', store_id=store_id))
	else:
		return render_template('deleteInventoryItem.html', item=itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)