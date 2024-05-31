"""Seed file to make sample data for all portions of the blog's db."""

from models import User, db, Post, Tag, PostTag
from sqlalchemy.sql import text
from app import app

# Push the application context
with app.app_context():
    # Drop all tables with cascade
    db.session.execute(text('DROP TABLE IF EXISTS post_tags CASCADE'))
    db.session.execute(text('DROP TABLE IF EXISTS posts CASCADE'))
    db.session.execute(text('DROP TABLE IF EXISTS users CASCADE'))
    db.session.execute(text('DROP TABLE IF EXISTS tags CASCADE'))
    db.session.commit()
    
    # Create all tables
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

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

    # Add tags
    tag1 = Tag(name='Fresh')
    tag2 = Tag(name='Old')
    tag3 = Tag(name='Dogs')
    tag4 = Tag(name='Cats')

    # Add new objects to session, so they'll persist
    db.session.add_all([tag1, tag2, tag3, tag4])

    # Commit--otherwise, this never gets saved!
    db.session.commit()

    # Link posts and tags
    post_tag1 = PostTag(post_id='1', tag_id='1')
    post_tag2 = PostTag(post_id='3', tag_id='1')
    post_tag3 = PostTag(post_id='2', tag_id='2')
    post_tag4 = PostTag(post_id='1', tag_id='4')

    # Add new objects to session, so they'll persist
    db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4])

    # Commit--otherwise, this never gets saved!
    db.session.commit()