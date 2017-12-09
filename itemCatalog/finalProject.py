"""This module is the flask application to serve, route http requests"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import random
import string
import json
import requests

app = Flask(__name__)

# Load client secret details for Google OAuth API
GOOGLE_CLIENT_ID = json.loads(
    open('google_client_secret.json', 'r').read())['web']['client_id']
GOOGLE_APP_NAME = "Restaurant Menu Application"

# connect to the database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories')
def showCategories():
    """serve all the available categories in database"""
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template("publicCategories.html", categories=categories)
    return render_template("categories.html", categories=categories)


@app.route('/category/add', methods=['GET', 'POST'])
def addCategory():
    """Process requests to add new category"""
    # authentication
    if 'username' not in login_session:
        flash('Please login to add category')
        return redirect(url_for('showCategories'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        # validation
        if not name:
            flash('Add CategoryError: Name can\'t be empty')
            return redirect(url_for('showCategories'))
        # create operation
        newCategory = Category(name=name, description=description,
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('Added Category \'{}\' Successfully!'.format(newCategory.name))
        return redirect(url_for('showCategories'))
    else:
        # serve GET request with form
        return render_template("addCategory.html")


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    """Process requests to edit existing category

    arguments:
    category_id(int)
    """
    # authentication
    if 'username' not in login_session:
        flash('Please login to edit category')
        return redirect(url_for('showCategories'))

    # validation
    editedCategory = session.query(Category).filter_by(id=category_id).first()
    if not editedCategory:
        flash('Attempt to edit non-existent category')
        return redirect(url_for('showCategories'))

    # authorization
    if login_session['user_id'] != editedCategory.user_id:
        flash('Sorry, you are not authorized to edit the category \'{}\''
              .format(editedCategory.name))
        return redirect(url_for('showItems', category_id=category_id))

    if request.method == 'POST':
        # update operation
        if request.form['name']:
            editedCategory.name = request.form['name']

        if request.form['description']:
            editedCategory.description = request.form['description']
        else:
            editedCategory.description = ''
        session.add(editedCategory)
        session.commit()
        flash('Edited Category \'{}\'  Successfully'.format(
            editedCategory.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        # serve GET requests with form
        return render_template("editCategory.html", category=editedCategory)


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """Process requests to delete category

    arguments:
    category_id(int)
    """
    # authentication
    if 'username' not in login_session:
        flash('Please login to edit category')
        return redirect(url_for('showCategories'))

    # validation
    deletedCategory = session.query(Category).filter_by(id=category_id).first()
    if not deletedCategory:
        flash('Attempt to delete non-existent category')
        return redirect(url_for('showCategories'))

    # authorization
    if login_session['user_id'] != deletedCategory.user_id:
        flash('Sorry, you are not authorized to delete the category \'{}\''
              .format(deletedCategory.name))
        return redirect(url_for('showCategories'))

    # delete operation
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash('Deleted Category \'{}\'  Successfully'.format(
            deletedCategory.name))
        return redirect(url_for('showCategories'))
    else:
        # serve GET requests with confirmation form
        return render_template("deleteCategory.html", category=deletedCategory)


@app.route('/category/<int:category_id>', methods=['GET', 'POST'])
@app.route('/category/<int:category_id>/items', methods=['GET', 'POST'])
def showItems(category_id):
    """Serve all items of the category

    arguments:
    category_id(int)
    """
    # validation
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        flash('Attempt to view non-existent category')
        return redirect(url_for('showCategories'))

    # authorization
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session or\
            login_session['user_id'] != category.user_id:
        return render_template("publicShowItems.html", category=category,
                               items=items)

    return render_template("showItems.html", category=category, items=items,
                           logged_in_user_id=login_session['user_id'])


@app.route('/category/<int:category_id>/item/add', methods=['GET', 'POST'])
def addItem(category_id):
    """Process requests to add new item to existing category

    arguments:
    category_id(int)
    """
    # authentication
    if 'username' not in login_session:
        flash('Please login to add item')
        return redirect(url_for('showItems', category_id=category_id))

    # validation
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))

    if request.method == 'POST':
        # create operation
        name = request.form['name']
        description = request.form['description']
        if not name:
            flash('Add ItemError: Name can\'t be empty')
            return redirect(url_for('showItems', category_id=category_id))
        newItem = Item(name=name, description=description,
                       category_id=category_id, user_id=category.user_id)
        session.add(newItem)
        session.commit()
        flash('Added Item \'{}\' Successfully!'.format(newItem.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        # serve GET requests with the form
        return render_template("addItem.html", category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """Process requests to edit an item

    arguments:
    category_id(int)
    item_id(int)
    """
    # authentication
    if 'username' not in login_session:
        flash('Please login to edit item')
        return redirect(url_for('showItems', category_id=category_id))

    # validation
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))

    editedItem = session.query(Item).filter_by(id=item_id,
                                               category_id=category_id).first()
    if not editedItem:
        flash('Attempt to edit non-existent item')
        return redirect(url_for('showItems', category_id=category_id))

    # authorization
    if login_session['user_id'] != editedItem.user_id:
        flash('Sorry, you are not authorized to edit the item \'{}\''
              .format(editedItem.name))
        return redirect(url_for('showItems', category_id=category_id))

    if request.method == 'POST':
        # update operation
        if request.form['name']:
            editedItem.name = request.form['name']

        if request.form['description']:
            editedItem.description = request.form['description']
        else:
            editedItem.description = ''
        session.add(editedItem)
        session.commit()
        flash('Edited Item \'{}\'  Successfully'.format(editedItem.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        # serve GET requests with the form
        return render_template("editItem.html",
                               category=category, item=editedItem)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """Process requests to delete an item

    arguments:
    category_id(int)
    item_id(int)
    """
    # authentication
    if 'username' not in login_session:
        flash('Please login to add item')
        return redirect(url_for('showItems', category_id=category_id))

    # validation
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))

    deletedItem = session.query(Item).\
        filter_by(id=item_id, category_id=category_id).first()
    if not deletedItem:
        flash('Attempt to delete non-existent item')
        return redirect(url_for('showItems', category_id=category_id))

    # authorization
    if login_session['user_id'] != deletedItem.user_id:
        flash('Sorry, you are not authorized to delete the item \'{}\''
              .format(deletedItem.name))
        return redirect(url_for('showItems', category_id=category_id))

    if request.method == 'POST':
        # delete operation
        session.delete(deletedItem)
        session.commit()
        flash('Deleted Item \'{}\'  Successfully'.format(deletedItem.name))
        return redirect(url_for('showItems', category_id=category_id))
    else:
        # serve GET requests with confirmation form
        return render_template("deleteItem.html",
                               category=deletedItem.category, item=deletedItem)


@app.route('/login')
def showLogin():
    """Serve login page for OAuth authentication"""
    # crate anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """validate and exchange authorization code from the client,
     to get access token"""
    # Validate state token for CSFP
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get authorization code from client
    code = request.data

    try:
        # Get access token using client auth code and app creds
        oauth_flow = flow_from_clientsecrets('google_client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to get the access token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        username = login_session['username']
        if username is None or len(username) == 0:
            username = login_session['email'].split('@')[0]
            login_session['username'] = username
        user_id = createUser(login_session)
    else:
        login_session['username'] = getUserInfo(user_id).name

    login_session['user_id'] = user_id

    # welcome message
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print('done!')
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """revokes access token and cleans up login session data"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        flash('Current user not connected.')
        return redirect(url_for('showCategories'))
    # print('Got access token for the user: {}'.
    #       format(login_session['username']))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %\
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print('Access token revoke result:{}'.format(result))
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully logged out')
        return redirect(url_for('showCategories'))
    else:
        flash('Failed to revoke token for given user.')
        return redirect(url_for('showCategories'))


def createUser(login_session):
    """Helper funtion to create new user on first login
    arguments:
    login_session(Flask session.login_session)
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Helper function to get existing user's details"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """helper funtion to get user.id using email"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# JSON Endpoint functions


@app.route('/categories/JSON')
def getCategoriesJSON():
    """serves all the categories in JSON format"""
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


@app.route('/category/<int:category_id>/JSON')
def getCategoryJSON(category_id):
    """serves requested category in JSON format
    arguments:
    category_id(int)
    """
    category = session.query(Category).filter_by(id=category_id).first()
    if category:
        return jsonify(Category=category.serialize)
    else:
        return jsonify(Category={})


@app.route('/category/<int:category_id>/items/JSON')
def getItemsJSON(category_id):
    """serves all the items in the requested category, in JSON format
    arguments:
    category_id(int)
    """
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def getItemJSON(category_id, item_id):
    """serves requested item of the given category in JSON format
    arguments:
    category_id(int)
    item_id(int)
    """
    item = session.query(Item).filter_by(id=item_id,
                                         category_id=category_id).first()
    if item:
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Item={})


# start flask server
if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\x87{\xfc\xc9\x94\x10.\x12$R\x1b\x8d\x8a\xe2\x81\x82'
    app.run(host='0.0.0.0', port=8100)
