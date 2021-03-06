from models import db, User
from app import app

# Re-create tables
db.drop_all()
db.create_all()

# Empty tables in case they aren't
User.query.delete()

# Add user records
user1 = User(first_name="User", last_name="1")
user2 = User(first_name="User", last_name="2")
user3 = User(first_name="User", last_name="3")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()