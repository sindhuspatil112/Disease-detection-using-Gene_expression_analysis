#!/usr/bin/env python3
"""
Demo setup script for GeneRisk AI
Creates sample users for testing role-based access
"""

from backend.app import create_app
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash

def create_demo_users():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Demo users
        demo_users = [
            {
                'name': 'John Patient',
                'email': 'patient@demo.com',
                'password': 'demo123',
                'role': 'user'
            },
            {
                'name': 'Dr. Sarah Wilson',
                'email': 'doctor@demo.com', 
                'password': 'demo123',
                'role': 'doctor'
            },
            {
                'name': 'Prof. Mike Research',
                'email': 'researcher@demo.com',
                'password': 'demo123', 
                'role': 'researcher'
            },
            {
                'name': 'Admin User',
                'email': 'admin@demo.com',
                'password': 'demo123',
                'role': 'admin'
            }
        ]
        
        for user_data in demo_users:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=generate_password_hash(user_data['password']),
                    role=user_data['role']
                )
                db.session.add(user)
                print(f"Created {user_data['role']} user: {user_data['email']}")
            else:
                print(f"User {user_data['email']} already exists")
        
        db.session.commit()
        print("\nDemo users created successfully!")
        print("\nLogin credentials:")
        print("Patient: patient@demo.com / demo123")
        print("Doctor: doctor@demo.com / demo123") 
        print("Researcher: researcher@demo.com / demo123")
        print("Admin: admin@demo.com / demo123")

if __name__ == "__main__":
    create_demo_users()