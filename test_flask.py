from unittest import TestCase
from datetime import datetime

from app import app
from models import db, User, Post

# Use the testing DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Re-create the tables
db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ Tests for the User views """

    def setUp(self):
        """ Add a sample user and post before each view """

        Post.query.delete()
        User.query.delete()

        # no image_url attr so we can test for default image
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Test Post", content="This is a test post", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """ Cleanup (rollback) any fouled transactions """

        db.session.rollback()
    
    def test_list_users(self):
        """ Tests the all users page """

        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)

    def test_show_user(self):
        """ Tests the user details page """

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Doe</h1>', html)

    def test_add_user(self):
        """ Tests the adding of a new user """
    
        with app.test_client() as client:
            d = {"first_name": "Joe", "last_name": "Shmoe"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Joe Shmoe", html)

    def test_show_edit_user(self):
        """ Tests the edit user form """
        
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" class="form-control mb-3" value="John" name="first_name" maxlength="20" required>', html)

            # Tests for default image_url
            self.assertIn('<input type="text" class="form-control mb-3" value="https://community.swordsandravens.net/ext/dark1/memberavatarstatus/image/avatar.png" name="image_url">', html)

    def test_add_post(self):
        """ Tests the adding of a new post """

        with app.test_client() as client:
            d = {"title": "new post", "content": "adding a new post!", "user_id": self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new post', html)
            self.assertIn('Test Post', html)

    def test_show_post(self):
        """ Tests the post details route """

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('This is a test post', html)
    
    def test_edit_post(self):
        """ Tests the editing of a post """

        with app.test_client() as client:
            d = {"title": "Edited post", "content": ""}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edited post", html)

    def test_delete_post(self):
        """ Tests the deletion of a post """

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('This is a test post', html)

            # Test that it was removed from the DB as well
            self.assertIsNone(Post.query.get(self.post_id))