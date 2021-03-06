"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
                    auto_increment=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, default="https://community.swordsandravens.net/ext/dark1/memberavatarstatus/image/avatar.png")

    def __repr__(self):
        """ Defines string representation of every User instance """
        return f"<User id={self.id} name={self.first_name} {self.last_name} image={self.image_url}"

    