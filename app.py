"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

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

    return render_template('/user_listing.html', users=users_from_db,)


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

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<user_id>")
def display_user_info(user_id):
    """ Shows information on user """
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<user_id>/edit")
def display_edit_user_form(user_id):
    """ Shows form for editing user info """
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user)


@app.route("/users/<user_id>/edit", methods=['POST'])
def handle_edit_user(user_id):
    """ Handle the submission of the edit user form """
    user = User.query.get(user_id)
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
    # would be adding NULL in psql, or add str of default image. set my default image to a const dont need to repeat

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


@app.route('/users/<user_id>/posts/new')
def show_add_post_form(user_id):
    """ Renders add post form"""

    user = User.query.get(user_id) # consider changing to get 404

    return render_template("new_post_form.html", user=user)


@app.route('/users/<user_id>/posts/new', methods=['POST'])
def handle_add_post(user_id):
    """ Handle the adding of a new post"""

    post_title = request.form["post-title"]
    post_content = request.form["post-content"]

    post = Post(title=post_title, content=post_content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    """ Show a post"""

    post = Post.query.get(post_id) # consider changing to get 404

    return render_template('/post_detail.html', post=post)


@app.route('/posts/<post_id>/edit')
def show_post_edit_form(post_id):
    """ Shows form to edit a post"""

    post = Post.query.get(post_id)

    return render_template('edit_post_form.html', post=post)


@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """ Handle the submission of the edit post form """

    post_title = request.form["post-title"]
    post_content = request.form["post-content"]
    post = Post.query.get(post_id)

    post.title = post_title
    post.content = post_content

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def handle_post_delete(post_id):
    """ Handle the deletion of a post """

    post = Post.query.get(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
