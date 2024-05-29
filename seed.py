"""Seed file to make sample data for users db."""

from models import User, db, Post
from app import app

# Push the application context
with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()

    # Add users
    user1 = User(first_name='Benjamin', last_name='Eng', image_url="https://images.unsplash.com/photo-1603415526960-f7e0328c63b1?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    user2 = User(first_name='Cindy', last_name='Li')
    user3 = User(first_name='Lola', last_name='Johnson')

    # Add new objects to session, so they'll persist
    db.session.add_all([user1, user2, user3])

    # Commit--otherwise, this never gets saved!
    db.session.commit()

    # Add posts
    post1 = Post(title="Ben's first post", content="I made a post", user_id="1")
    post2 = Post(title="Ben's second post", content="I made another post", user_id="1")
    post3 = Post(title="Cindy's first post", content="I made a post", user_id="2")
    post4 = Post(title="Cindy's second post", content="I made another post", user_id="2")
    post5 = Post(title="Lola's favorite post", content="I made this great post", user_id="3")
    post6 = Post(title="Ben's latest post", content="Here is another update", user_id="1")

    # Add new objects to session, so they'll persist
    db.session.add_all([post1, post2, post3, post4, post5, post6])

    # Commit--otherwise, this never gets saved!
    db.session.commit()