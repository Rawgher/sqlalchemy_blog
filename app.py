"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
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

@app.route("/")
def home():
    return redirect('/users')

@app.route("/users")
def all_users():
    """List all users in the database"""

    users = User.query.all()
    return render_template("user-list.html", users=users)

@app.route("/users/new")
def new_user():
    """Show new user form"""
    return render_template("new-user.html")

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

@app.route("/users/<int:user_id>")
def single_user(user_id):
    """Show a single user account"""

    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show a single user account"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

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

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')