import os
from app import app, db
from app import User, LeaveType
from werkzeug.security import generate_password_hash

def reset_database():
    # Get the database file path
    db_file = 'users.db'
    uploads_dir = 'uploads'
    
    # Remove the database file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database: {db_file}")
    
    # Remove all files in uploads directory
    if os.path.exists(uploads_dir):
        for file in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
        print("Cleared uploads directory")
    
    # Create the uploads directory if it doesn't exist
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Create new database and tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create test users with different hierarchy levels
        users = [
            {
                'email': 'admin@example.com',
                'password': 'admin123',
                'name': 'Admin User',
                'department': 'Management',
                'hierarchy_level': 3  # Admin
            },
            {
                'email': 'head@example.com',
                'password': 'head123',
                'name': 'Department Head',
                'department': 'IT',
                'hierarchy_level': 2  # Head
            },
            {
                'email': 'manager@example.com',
                'password': 'manager123',
                'name': 'IT Manager',
                'department': 'IT',
                'hierarchy_level': 1  # Manager
            },
            {
                'email': 'employee@example.com',
                'password': 'employee123',
                'name': 'IT Employee',
                'department': 'IT',
                'hierarchy_level': 0  # Employee
            }
        ]
        
        for user_data in users:
            user = User(
                email=user_data['email'],
                password=generate_password_hash(user_data['password']),
                name=user_data['name'],
                department=user_data['department'],
                hierarchy_level=user_data['hierarchy_level']
            )
            db.session.add(user)
        
        # Create default leave types
        leave_types = [
            {'name': 'Annual Leave', 'default_days': 20, 'color_code': '#28a745'},
            {'name': 'Sick Leave', 'default_days': 12, 'color_code': '#dc3545'},
            {'name': 'Casual Leave', 'default_days': 6, 'color_code': '#ffc107'}
        ]
        
        for leave_type_data in leave_types:
            leave_type = LeaveType(**leave_type_data)
            db.session.add(leave_type)
        
        db.session.commit()
        print("Database reset completed successfully!")
        print("\nCreated test users:")
        for user in users:
            print(f"Email: {user['email']}")
            print(f"Password: {user['password']}")
            print(f"Role: {['Employee', 'Manager', 'Head', 'Admin'][user['hierarchy_level']]}")
            print()

if __name__ == "__main__":
    reset_database() 