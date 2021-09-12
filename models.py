from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to the provided Flask app."""
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
default_img = "https://icon-library.com/images/icon-portrait/icon-portrait-2.jpg"


class User (db.Model):
    """Model for a user on the site."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_img)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return the user's full name."""

        return f"{self.first_name} {self.last_name}"


class Post (db.Model):
    """Model for a blog post on the site."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def formatted_date(self):
        """Returns the date and time in a nice and readable format."""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class PostTag (db.Model):
    """Tag added on a post."""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """A tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags",
    )
