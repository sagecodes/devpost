#devpost
 This was a submission for project 3 of Udacity's Fullstack nanodegree. The main focus for this project was building the Flask backend so please excuse the rushed design.

The project allows a user to login via a Google account using Oauth2 and create profiles containing a picture, contact info and any projects they would like to show. Each project take a name, picture, description, github URL, and a live demo URL.

##Requirements:
The project was tested and developed with:

* flask 0.10.1 and flask version dependencies (Jinja, etc)
* python 2.7.10
* SQL Alchemy 1.0
* oauth2client
* SQLite3
* requests

## Notes for grading:
Requirements should be met within the default udacity vagrant setup, but if any problem arises please check imports vs what you have installed.

Category = profile

Project = catalog item

Main.py should comply with PEP8 standards except camelCase function and variable names due to the style of code in teaching.

##Running the project
* Clone/download the project files to an environment where requirements are met.

* click login link in navigation to be taken to login page

* navigate to project folder and run main.py `python main.py`

* Login with google account

* Once logged in a link will be added to navigation bar to add new profile

* Once you add a new profile you can create new projects within the profile page

* edit and delete links will appear at the bottom of each project you create

* edit and delete profile links are found at the bottom of the profile pages

* please see API section in main.py for JSON endpoints


## Authors
Sage Elliott

hello@sageelliott.com