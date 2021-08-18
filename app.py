"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/users')
def homepage():
    """List all users."""
    users = User.query.all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def new_user():
    """Form to add a new user."""

    return render_template('create_user.html')


@app.route('/users', methods=['POST'])
def create_new_user():
    """Create a new user."""
    first_name = request.form['f_name']
    last_name = request.form['l_name']
    image = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a specific user."""
    user = User.query.get_or_404(user_id)

    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def update_user(user_id):
    """Get the edit form for an existing user."""
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['f_name']
    user.last_name = request.form['l_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete an existing user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
