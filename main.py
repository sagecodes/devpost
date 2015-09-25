from flask import Flask, render_template, request, redirect, url_for

from database_setup import Base, Profile, Project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


# Database operations
#=======================================================================

# create Session and connect to database
engine = create_engine('sqlite:///devpost.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

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
def deleteProfile():
    return "hello"


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
    return "Create new Project for a profile"


# Edit an existing project for selected profile
@app.route('/profile/<int:profile_id>/project/<int:project_id>/edit/',
 methods=['GET', 'POST'])
def editProject(profile_id, project_id):
    return "Edit Project for a profile"


# Delete an existing project for a selected profile
@app.route('/profile/<int:profile_id>/project/<int:project_id>/delete/',
 methods=['GET', 'POST'])
def deleteProject(profile_id, project_id):
    return "Delete Project for a profile"



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 3000)