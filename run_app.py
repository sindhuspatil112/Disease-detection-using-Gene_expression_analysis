#!/usr/bin/env python3
"""
Quick start script for GeneRisk AI
"""

import os
import sys
from backend.app import create_app
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash

def setup_and_run():
    print("🧬 Starting GeneRisk AI...")
    
    app = create_app()
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database initialized")
        
        # Create demo users
        demo_users = [
            {'name': 'John Patient', 'email': 'patient@demo.com', 'password': 'demo123', 'role': 'user'},
            {'name': 'Dr. Sarah Wilson', 'email': 'doctor@demo.com', 'password': 'demo123', 'role': 'doctor'},
            {'name': 'Prof. Mike Research', 'email': 'researcher@demo.com', 'password': 'demo123', 'role': 'researcher'},
            {'name': 'System Admin', 'email': 'admin@demo.com', 'password': 'admin123', 'role': 'admin'}
        ]
        
        created_count = 0
        for user_data in demo_users:
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=generate_password_hash(user_data['password']),
                    role=user_data['role']
                )
                db.session.add(user)
                created_count += 1
                print(f"Created: {user_data['email']}")
        
        if created_count > 0:
            db.session.commit()
            print(f"✅ {created_count} demo users created")
        else:
            print("✅ Demo users already exist")
    
    print("\n🚀 GeneRisk AI is running!")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("\n🔐 Demo Login Credentials:")
    print("   Patient: patient@demo.com / demo123")
    print("   Doctor: doctor@demo.com / demo123")
    print("   Researcher: researcher@demo.com / demo123")
    print("   Admin: admin@demo.com / admin123")
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    setup_and_run()