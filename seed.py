"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Push the application context
with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add users
    user1 = User(first_name='Benjamin', last_name='Eng', image_url="https://images.unsplash.com/photo-1603415526960-f7e0328c63b1?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    user2 = User(first_name='Cindy', last_name='Li')
    user3 = User(first_name='Lola', last_name='Johnson')

    # Add new objects to session, so they'll persist
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # Commit--otherwise, this never gets saved!
    db.session.commit()
