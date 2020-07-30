"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

@app.route("/")
def index():
    """ Redirects to list of users """

    return redirect('/users')

@app.route("/users")
def users_listing():
    """ Redirects to list of users """

    # users_from_db = query all users from DB
    users_from_db = User.query.all()

    return render_template('/user_listing.html', users = users_from_db,)

@app.route("/users/new")
def show_new_user_form():
    """ Shows an add new user form """
    return render_template("new_user_form.html")

@app.route("/users/new", methods=['POST'])
def handle_new_user():
    """ Handle the submission of the new user form """
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png' 

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<user_id>")
def display_user_info(user_id):
    """ Shows information on user """
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user = user)

@app.route("/users/<user_id>/edit")
def display_edit_user_form(user_id):
    """ Shows form for editing user info """
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user = user)

@app.route("/users/<user_id>/edit", methods=['POST'])
def handle_edit_user(user_id):
    """ Handle the submission of the edit user form """
    user = User.query.get(user_id)
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png' 
    # would be adding NULL in psql, or add str of default image

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url 

    db.session.commit()

    return redirect("/users")

@app.route("/users/<user_id>/delete", methods=['POST'])
def handle_delete_user(user_id):
    """ Handle the deleting of a user """
    user_id = request.form["delete-user"]
    user = User.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")