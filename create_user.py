#!/usr/bin/env python3
from backend.app import create_app
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Create a test user
    if not User.query.filter_by(email='test@demo.com').first():
        user = User(
            name='Test User',
            email='test@demo.com',
            password=generate_password_hash('123'),
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Created test user: test@demo.com / 123")
    else:
        print("User already exists")
        
    # List all users
    users = User.query.all()
    print(f"\n📋 Total users in database: {len(users)}")
    for u in users:
        print(f"  - {u.email} ({u.role})")