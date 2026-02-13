#!/usr/bin/env python3
from backend.app import create_app
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Delete existing admin if exists
    existing_admin = User.query.filter_by(email='admin@demo.com').first()
    if existing_admin:
        db.session.delete(existing_admin)
        db.session.commit()
    
    # Create new admin user
    admin = User(
        name='System Admin',
        email='admin@demo.com',
        password=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Admin user created successfully!")
    print("Email: admin@demo.com")
    print("Password: admin123")
    
    # List all users to verify
    users = User.query.all()
    print(f"\n📋 All users in database:")
    for u in users:
        print(f"  - {u.email} ({u.role})")