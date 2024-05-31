"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# GET ROUTES --------------------------------------------------

@app.route("/")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route("/users")
def all_users():
    """List all users in the database"""

    users = User.query.all()
    return render_template("user/user-list.html", users=users)

@app.route("/users/new")
def new_user():
    """Show new user form"""
    return render_template("user/new-user.html")

@app.route("/users/<int:user_id>")
def single_user(user_id):
    """Show a single user account"""

    user = User.query.get_or_404(user_id)
    return render_template("user/user.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show a single user account"""

    user = User.query.get_or_404(user_id)
    return render_template("user/edit-user.html", user=user)

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show new post form"""
    user = User.query.get_or_404(user_id)
    return render_template("posts/new-post.html")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show individual post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show a single user account"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit-post.html", post=post)

@app.route("/tags")
def all_tags():
    """List all tags in the database"""

    tags = Tag.query.all()
    return render_template("tags/tags-list.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def current_tag(tag_id):
    """Show single tag and all its associated posts from the database"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/tag.html", tag=tag)

@app.route("/tags/new")
def new_tag_form():
    """Show new tag form"""
    return render_template("tags/new-tag.html")

# POST ROUTES -------------------------------------------------

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add a new user to the database"""

    first = request.form['first']
    last = request.form['last']
    pic_url = request.form['pic-url']

    user = User(first_name=first, last_name=last, image_url=pic_url)

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit a user and submit to the database"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['pic-url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add a new post to the database"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit a post and submit to the database"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Add a new tag to the database"""

    name = request.form['name']

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

# DELETE ROUTES -----------------------------------------------

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Deletes a post from the database"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')