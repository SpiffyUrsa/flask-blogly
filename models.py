"""Demo file showing off a model for SQLAlchemy."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__="users"

    id = db.Column(db.Integer, 
        primary_key=True, 
        autoincrement=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    image_url = db.Column(db.String(100), 
        nullable=False, # will there be a difference between how to handle '' vs NULL?
        default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

class Post(db.Model):
    """Post."""

    __tablename__="posts"

    user = db.relationship('User', backref='posts')

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(9001), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    ## CODEREVIEW: at a db-level, line 44 sets our referential constraint
