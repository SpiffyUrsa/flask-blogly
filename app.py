"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
