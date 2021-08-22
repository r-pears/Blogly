from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    """Tests for views for User and Post."""

    def setUp(self):
        """Add sample user and post."""

        User.query.delete()
        Post.query.delete()

        test_user = User(first_name="John", last_name="Smith")
        test_post = Post(title='Test', content="My content", user_id=1)

        db.session.add(test_user)
        db.session.commit()

        db.session.add(test_post)

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Smith</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Ellen", "last_name": "Keyes"}
            resp = client.post("/users", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Ellen Keyes</h1>", html)
