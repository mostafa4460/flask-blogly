"""Seed file for blogly DB"""

from models import db, User, Post
from app import app

# Re-create tables
db.drop_all()
db.create_all()

# Empty tables in case they aren't
User.query.delete()

# Add user records
user1 = User(first_name="John", last_name="Doe")
user2 = User(first_name="Joe", last_name="Shmoe")
user3 = User(first_name="Success", last_name="Baby", image_url="https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,fl_progressive,g_center,h_675,pg_1,q_80,w_1200/ynp10svzrvtwadgusinj.png")

db.session.add_all([user1, user2, user3])
db.session.commit()

# Add post records
post1 = Post(title="My first post", content="I really don't know what to write here ...", user_id=1)
post2 = Post(title="My first post", content="I really don't know what to write here ...", user_id=2)
post3 = Post(title="My first post", content="I really don't know what to write here ...", user_id=3)

db.session.add_all([post1, post2, post3])
db.session.commit()