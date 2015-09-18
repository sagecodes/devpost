from flask import Flask

app = Flask(__name__)


#list of profiles created by users
@app.route('/')
@app.route('/profiles/')
def Profiles():
    return "List profiles"


# Create a new profile
@app.route('/profile/new')
def NewProfile():
    return "Create a new profile"


# Edit an exsisting profile
#<int:profile_id>
@app.route('/profile/1/edit/', methods=['GET', 'POST'])
def EditProfile():
    return "Edit a profile"


# Delete an exsisting profile
#<int:profile_id>
@app.route('/profile/1/delete/', methods=['GET', 'POST'])
def DeleteProfile():
    return "Delete a profile"



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 3000)