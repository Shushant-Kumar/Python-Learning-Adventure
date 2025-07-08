"""
Database Migration Script
Adds the is_admin column to the users table
"""

import sqlite3
import os

def migrate_database():
    """Add is_admin column to users table if it doesn't exist."""
    db_path = 'python_learning.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database not found. Please run the application first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if is_admin column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' not in columns:
            print("Adding is_admin column to users table...")
            
            # Add the is_admin column
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            
            # Set the first user (admin) to be an admin
            cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
            
            conn.commit()
            print("✅ Database migration completed successfully!")
            print("✅ Admin column added to users table")
            
            # Show admin users
            cursor.execute("SELECT username, email, is_admin FROM users WHERE is_admin = 1")
            admin_users = cursor.fetchall()
            if admin_users:
                print("\nAdmin users:")
                for user in admin_users:
                    print(f"  - {user[0]} ({user[1]})")
            else:
                print("\nNo admin users found. You may need to manually set a user as admin.")
        else:
            print("✅ is_admin column already exists in users table")
            
            # Show current admin users
            cursor.execute("SELECT username, email, is_admin FROM users WHERE is_admin = 1")
            admin_users = cursor.fetchall()
            if admin_users:
                print("\nCurrent admin users:")
                for user in admin_users:
                    print(f"  - {user[0]} ({user[1]})")
            else:
                print("\nNo admin users found.")
                
                # Ask if we should make the first user admin
                cursor.execute("SELECT username FROM users LIMIT 1")
                first_user = cursor.fetchone()
                if first_user:
                    response = input(f"\nMake '{first_user[0]}' an admin? (y/n): ").lower()
                    if response == 'y':
                        cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (first_user[0],))
                        conn.commit()
                        print(f"✅ {first_user[0]} is now an admin!")
    
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
