from flask import Flask, render_template, request, redirect, url_for, flash

from database_setup import Base, Profile, Project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


# Database operations
#=======================================================================

# create Session and connect to database
engine = create_engine('sqlite:///devpost.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Authentication and Authorization
#=======================================================================

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "devpost"

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                                                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token:
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credential object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If error in access token info abort:
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # verify access token is used for intended user
    gplus_id = credentials.id_token['sub']
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
    #check to see if user is already logged in:
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # # check if user exists, if not create new user:
    # user_id = getUserId(login_session['email'])
    # if not user_id:
    #     user_id = createUser(login_session)
    # login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route("/gdisconnect/")
def gdisconnect():
    #only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps("Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Profile operations
#=======================================================================

#list of profiles created by users
@app.route('/')
@app.route('/profiles/')
def showProfiles():
    profiles = session.query(Profile).all()
    return render_template('profiles.html', profiles=profiles)


# Create a new profile
@app.route('/profile/new/' , methods=['GET', 'POST'])
def newProfile():
    if request.method == 'POST':
        newProfile = Profile(name = request.form['name'],
        picture = request.form['picture'], email = request.form['email'],
        github = request.form['github'], twitter = request.form['twitter'] )
        session.add(newProfile)
        session.commit()
        return redirect(url_for('showProfiles'))
    else:
        return render_template('newProfile.html')


# Edit an exsisting profile
@app.route('/profile/<int:profile_id>/edit/', methods=['GET', 'POST'])
def editProfile(profile_id):
    editProfile = session.query(Profile).filter_by(id = profile_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editProfile.name = request.form['name']
        if request.form['picture']:
            editProfile.picture = request.form['picture']
        if request.form['email']:
            editProfile.email = request.form['email']
        if request.form['github']:
            editProfile.github = request.form['github']
        if request.form['twitter']:
            editProfile.twitter = request.form['twitter']
        session.add(editProfile)
        session.commit()
        return redirect(url_for('showProfiles'))
    else:
        return render_template('editProfile.html', profile=editProfile)


# Delete an exsisting profile
@app.route('/profile/<int:profile_id>/delete/', methods=['GET', 'POST'])
def deleteProfile(profile_id):
    deleteProfile = session.query(Profile).filter_by(id = profile_id).one()
    if request.method == 'POST':
        session.delete(deleteProfile)
        session.commit()
        return redirect(url_for('showProfiles'))
    else:
        return render_template('deleteProfile.html', profile=deleteProfile)


# Project operations
#=======================================================================

# Show list of project for a selected profile
@app.route('/profile/<int:profile_id>/')
@app.route('/profile/<int:profile_id>/projects/')
def showProjects(profile_id):
    profile = session.query(Profile).filter_by(id = profile_id).one()
    projects = session.query(Project).filter_by(profile_id = profile.id).all()
    return render_template('projects.html', profile=profile, projects=projects)


# Create a new project for selected profile
@app.route('/profile/<int:profile_id>/project/new/', methods=['GET', 'POST'])
def newProject(profile_id):
    profile = session.query(Profile).filter_by(id = profile_id).one()
    if request.method == 'POST':
        newProject = Project(name = request.form['name'],
                            picture = request.form['picture'],
                            description = request.form['description'],
                            sourcecode = request.form['sourcecode'],
                            livedemo = request.form['livedemo'],
                            profile_id = profile_id)
        session.add(newProject)
        session.commit()
        return redirect(url_for('showProjects', profile_id = profile_id))
    else:
        return render_template('newProject.html', profile=profile)


# Edit an existing project for selected profile
@app.route('/profile/<int:profile_id>/project/<int:project_id>/edit/',
 methods=['GET', 'POST'])
def editProject(profile_id, project_id):
    profile = session.query(Profile).filter_by(id = profile_id).one()
    editProject = session.query(Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editProject.name = request.form['name']
        if request.form['picture']:
            editProject.picture = request.form['picture']
        if request.form['description']:
            editProject.description = request.form['description']
        if request.form['sourcecode']:
            editProject.sourcecode = request.form['sourcecode']
        if request.form['livedemo']:
            editProject.livedemo = request.form['livedemo']
        session.add(editProject)
        session.commit()
        return redirect(url_for('showProjects', profile_id = profile_id))
    else:
        return render_template('editProject.html', profile=profile,
        project=editProject)


# Delete an existing project for a selected profile
@app.route('/profile/<int:profile_id>/project/<int:project_id>/delete/',
 methods=['GET', 'POST'])
def deleteProject(profile_id, project_id):
    profile = session.query(Profile).filter_by(id = profile_id).one()
    deleteProject = session.query(Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        session.delete(deleteProject)
        session.commit()
        return redirect(url_for('showProjects', profile_id=profile_id))
    else:
        return render_template('deleteProject.html', profile=profile,
                                                    project = deleteProject)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 3000)