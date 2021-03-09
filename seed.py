"""Seed file for blogly DB"""

from models import db, User, Post, Tag, PostTag
from app import app

# Re-create tables
db.drop_all()
db.create_all()

# Empty tables in case they aren't
PostTag.query.delete()
Post.query.delete()
User.query.delete()
Tag.query.delete()

# Add user and post records
user1 = User(first_name="John", last_name="Doe")
user2 = User(first_name="Joe", last_name="Shmoe")
user3 = User(first_name="Success", last_name="Baby", image_url= "https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,fl_progressive,g_center,h_675,pg_1,q_80,w_1200/ynp10svzrvtwadgusinj.png")

post1 = Post(title="My 1st post", content="I really don't know what to write here ...", owner=user1)
post2 = Post(title="My 1st post", content="I really don't know what to write here ...", owner=user2)
post3 = Post(title="My 1st post", content="I really don't know what to write here ...", owner=user3)
post4 = Post(title="My 2nd post", content="I still don't know what to write here ...", owner=user1)
post5 = Post(title="My 1st/2nd post", content="I still don't know what to write here ...", owner=user2)
post6 = Post(title="My 2nd post", content="I still don't know what to write here ...", owner=user3)

db.session.add_all([user1, user2, user3, post1, post2, post3, post4, post5, post6])
db.session.commit()

# Add tag records
tag1 = Tag(name="1st Posts", posts_tags=[
    PostTag(post_id=post1.id),
    PostTag(post_id=post2.id),
    PostTag(post_id=post3.id),
    PostTag(post_id=post5.id)
])
tag2 = Tag(name="2nd Posts", posts_tags=[
    PostTag(post_id=post4.id),
    PostTag(post_id=post5.id),
    PostTag(post_id=post6.id)
])

db.session.add_all([tag1, tag2])
db.session.commit()