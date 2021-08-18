from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
default_img = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'


class User (db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True, default=default_img)

    @property
    def full_name(self):
        """Return the full name of the user."""

        return f"{self.first_name} {self.last_name}"
