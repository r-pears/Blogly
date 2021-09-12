"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Show homepage with most recent posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route('/users')
def users():
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


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Get the form to create a new post for a specific user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts_new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    """Form submission for creating a new blog post."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post with a specific id."""
    post = Post.query.get_or_404(post_id)

    return render_template('show_post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Form submission for editing an existing post."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete')
def posts_destroy(post_id):
    """Delete an existing post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/tags')
def tags_index():
    """Show an index page with info about all available tags."""
    tags = Tag.query.all()

    return render_template('tags_index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag."""
    posts = Post.query.all()

    return render_template('tags_new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Form submission for creating a new tag."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")
