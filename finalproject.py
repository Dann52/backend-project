from flask import (
                Flask,
                render_template,
                request, redirect,
                url_for,
                flash,
                jsonify)

# import the SQLAlchemy code for our database
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, PlaceCategory, Place, User

# imports for oauth login
from flask import session as login_session
import random
import string


# creates a flow object form,
#  the clientsecrets json file.
from oauth2client.client import flow_from_clientsecrets
# use the FlowExchangeError method if we run,
# into an error trying to exchange an authorization code,
# for an access token
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# create an instance of Flask,
# with the name of the running application as the argument
app = Flask(__name__)


# store client_secrets in CLIENT_ID object
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Things To Do Application"

# the create engine function lets our program know
# which db engine we want to communicate with
engine = create_engine(
                        'sqlite:///places.db',
                        connect_args={'check_same_thread': False})

# makes the connection between our class definitions,
# and the cooresponding tables within the db
Base.metadata.bind = engine
# establishes a communication link between our,
# code executions and the engine we created
DBSession = sessionmaker(bind=engine)
session = DBSession()


# route to login to Google API
@app.route('/login')
def showLogin():
    # create state variable that contains a string that is
    # a mix of letters and numbers 32 digits long
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # store state in the login_session object under the name state
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # if the above statement is not true,
    # collect the one time state token from the server
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # specify with postmessage that this is the
        # one time code flow the server will be sending off
        oauth_flow.redirect_uri = 'postmessage'
        # initiate the exchange with the step2 exchange function,
        # pasing in the one time code
        credentials = oauth_flow.step2_exchange(code)
    # if there is an error, send error response as json object
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    # google api server can verify that this is a valid token for use
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

    # return error if 2 IDs do not match
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is\
                   already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the login_session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info using google API
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}

    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # store user info we're interested in in login session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check to see if user exists, if not make a new id
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; \
                height: 300px;\
                border-radius: 150px;\
                -webkit-border-radius: 150px;\
                -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    # if access_token is empty, we don't have a record of the user
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user\
                   not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    # pass the access token into google's url for revoking tokens
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    # store google's response in an object called result
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    # if result is successful, we have revoked the token and
    # can delete attributes of login_session object
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        # make response to indicate user successfully logged out of the session
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = (make_response(json.dumps
                    ('Failed to revoke token for given user.', 400)))
        response.headers['Content-Type'] = 'application/json'
        return response


# route that lists all activities in an area
@app.route('/')
@app.route('/thingstodo/')
def categoryList():
    categories = session.query(PlaceCategory).all()

    if 'username' not in login_session:
        return render_template('thingstodocategories_public.html', categories=categories)
    else:
        return render_template('thingstodocategories.html', categories=categories)


@app.route('/thingstodo/new/', methods=['GET', 'POST'])
def newCategory():
    # check to make sure user is logged in, if not redirect them to login page
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        # create a new item, extracting the name field from the form
        newCategory = PlaceCategory(name=request.form['name'], 
                      user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        # after this change has been made (session commmitted)
        # flash a message on the page
        flash("New Category Created!")
        # redirects to the url of the main page
        return redirect(url_for('categoryList', ))
    else:
        return render_template('newcategory.html', )


@app.route('/thingstodo/<int:category_id>/edit/', methods=['GET', 'POST'])
def editPlaceCategory(category_id):
    editCategory = (session.query(PlaceCategory).
                    filter_by(id=category_id).one())

    if editCategory.user_id != login_session['user_id']:
        return "<script>function alertFunction() {alert('You are not \
        authorized to edit this category. Please create your own category\
        in order to edit.');}</script><body onload='alertFunction()''>"

    # check to make sure user is logged in, if not redirect them to login page
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        editCategory.name = request.form['categoryName']
        session.add(editCategory)
        session.commit()

        flash(editCategory.name + " was edited!")
        return redirect(url_for('categoryList', ))
    else:
        return render_template(
                                'editcategory.html',
                                category=editCategory,
                                category_id=category_id)


@app.route('/thingstodo/<int:category_id>/delete/', methods=['GET', 'POST'])
def deletePlaceCategory(category_id):
    deleteCategory = (session.query(PlaceCategory).
                      filter_by(id=category_id).one())

    # check to make sure user is logged in,
    # if not redirect them to login page
    if 'username' not in login_session:
        return redirect('/login')

    if deleteCategory.user_id != login_session['user_id']:
        return "<script>function alertFunction() {alert('You are not \
        authorized to delete this category. Please create your own\
        category in order to be able to delete it.');}\
        </script><body onload='alertFunction()''>"

    if request.method == 'POST':

        session.delete(deleteCategory)
        session.commit()

        flash(deleteCategory.name + " was deleted!")

        return redirect(url_for('categoryList', ))
    else:
        return render_template(
                                'deletecategory.html',
                                category=deleteCategory,
                                category_id=category_id)


# route to an individual activity
@app.route('/thingstodo/<int:category_id>/')
def categoryPlaces(category_id):
    category = session.query(PlaceCategory).filter_by(id=category_id).one()

    creator = getUserInfo(category.user_id)

    places = session.query(Place).filter_by(category_id=category.id)

    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('thingstodo_public.html',
                                category=category, places=places)
    else: 
        return render_template('thingstodo.html',
                            category=category, places=places)


# route to a create a new individual activity within a category
@app.route('/thingstodo/<int:category_id>/new_place/',
           methods=['GET', 'POST'])
def newPlace(category_id):

    # if user is not logged in, redirect them to login page
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(PlaceCategory).filter_by(id=category_id).one()

    if login_session['user_id'] != category.user_id:
        return "<script>function alertFunction() {alert('You are not\
         authorized to add places to this category. Please create your\
          own category in order to add places.');}\
          </script><body onload='alertFunction()''>"

    if request.method == 'POST':
        # create a new place, extracting the name field from the form
        newPlace = Place(category_id=category_id)
        newPlace.name = request.form['placeName']
        newPlace.description = request.form['placeDescription']
        newPlace.price = request.form['placePrice']
        newPlace.user_id = category.user_id
        session.add(newPlace)
        session.commit()

        flash("New Place Created!")
        return redirect(url_for('categoryPlaces', category_id=category_id))
    else:
        return render_template('newplace.html', category_id=category_id)


@app.route('/thingstodo/<int:category_id>/<int:place_id>/edit_place/',
           methods=['GET', 'POST'])
def editPlace(category_id, place_id):

    category = session.query(PlaceCategory).filter_by(id=category_id).one()

    editPlace = (session.query(Place).
                 filter_by(category_id=category_id, id=place_id).one())

    if 'username' not in login_session:
        return redirect('/login')


    if login_session['user_id'] != category.user_id:
        return "<script>function alertFunction() {alert('You are not\
         authorized to edit places in this category. Please create your\
          own category in order to edit places.');}\
          </script><body onload='alertFunction()''>"

    if request.method == 'POST':

        placeName = request.form.get('placeName')
        placeDescription = request.form.get('placeDescription')
        placePrice = request.form.get('placePrice')

        # check to ensure each field has a value,
        # and if so edit the value accordingly
        if placeName:
            editPlace.name = request.form['placeName']
        if placeDescription:
            editPlace.description = request.form['placeDescription']
        if placePrice:
            editPlace.price = request.form['placePrice']
        session.add(editPlace)
        session.commit()

        flash(editPlace.name + " was edited.")

        return redirect(url_for('categoryPlaces', category_id=category_id))
    else:

        return render_template(
                                'editplace.html',
                                category_id=category_id,
                                place_id=place_id,
                                place=editPlace)


# route for deleting an individual place within a category
@app.route('/thingstodo/<int:category_id>/<int:place_id>/delete_place/',
           methods=['GET', 'POST'])
def deletePlace(category_id, place_id):
    deletePlace = (session.query(Place).
                   filter_by(category_id=category_id, id=place_id).one())
    category = session.query(PlaceCategory).filter_by(id=category_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if login_session['user_id'] != category.user_id:
        return "<script>function alertFunction() {alert('You are not\
         authorized to delete places in this category. Please\
          create your own category in order to delete places.');}\
          </script><body onload='alertFunction()''>"

    if request.method == 'POST':
        session.delete(deletePlace)
        session.commit()

        flash(deletePlace.name + " was deleted.")

        return redirect(url_for('categoryPlaces', category_id=category_id))

    else:
        return render_template(
                                'deleteplace.html',
                                category_id=category_id,
                                place_id=place_id,
                                place=deletePlace)


# Making an API endpoint (Get Request)
@app.route('/thingstodo/JSON')
def categoryJSON():
    categories = session.query(PlaceCategory).all()
    # instead of returning a template return jsonify class that
    # uses a for loop to serialize all db entries
    return jsonify(PlaceCategorys=[c.serialize for c in categories])


@app.route('/thingstodo/<int:category_id>/place/JSON')
def categoryPlacesJSON(category_id):
    # create query to obtain Place object that
    # contains all items from that category
    places = session.query(Place).filter_by(category_id=category_id).all()

    return jsonify(Places=[p.serialize for p in places])


# route for JSON data to display specific place
@app.route('/thingstodo/<int:category_id>/place/<int:place_id>/JSON')
def placeJSON(category_id, place_id):
    # create query to obtain Place object that
    # contains a specific place within a category
    place = (session.query(Place)
             .filter_by(category_id=category_id, id=place_id).one())

    return jsonify(onePlace=place.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
