"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """ Connects db to flask app """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User model"""

    __tablename__ = "users"
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, default="https://community.swordsandravens.net/ext/dark1/memberavatarstatus/image/avatar.png")

    def __repr__(self):
        """ Defines string representation of every User instance """
        return f"<User id={self.id} name={self.first_name} {self.last_name} image={self.image_url}>"

class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime("%m/%d/%Y %I:%M"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='posts')
    posts_tags = db.relationship('PostTag', backref='post')
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(self):
        """ Defines string representation of every Post instance """
        return f"<Post id={self.id} title={self.title} created_at={self.created_at}>"

class Tag(db.Model):
    """ Tag model """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    posts_tags = db.relationship('PostTag', backref='tag')

    def __repr__(self):
        """ Defines string representation of every Tag instance """
        return f"<Tag id={self.id} name={self.name}>"


class PostTag(db.Model):
    """ PostTag join model """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        """ Defines string representation of every PostTag instance """
        return f"<PostTag post_id={self.post_id} tag_id={self.tag_id}>"