from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class PetModelTestCase(TestCase):
    """Tests for model for User."""

    def setUp(self):
        """Clean up any existing user."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        user = User(first_name="John", last_name="Smith")
        self.assertEquals(user.full_name(), "John Smith")
