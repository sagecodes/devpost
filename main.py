from flask import Flask

app = Flask(__name__)

# dummy data

# Profile operations
#================================================

#list of profiles created by users
@app.route('/')
@app.route('/profiles/')
def showProfiles():
    return "List profiles"


# Create a new profile
@app.route('/profile/new/' , methods=['GET', 'POST'])
def newProfile():
    return "Create a new profile"


# Edit an exsisting profile
@app.route('/profile/<int:profile_id>/edit/', methods=['GET', 'POST'])
def editProfile():
    return "Edit a profile"


# Delete an exsisting profile
@app.route('/profile/<int:profile_id>/delete/', methods=['GET', 'POST'])
def deleteProfile():
    return "Delete a profile"


# Project operations
#================================================

# Show list of project for a selected profile
@app.route('/profile/<int:profile_id>/')
@app.route('/profile/<int:profile_id>/projects/')
def showProjects(profile_id):
    return "Show Projects for a profile"


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