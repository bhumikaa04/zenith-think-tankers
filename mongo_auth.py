# mongo_auth.py
import pymongo
from pymongo import MongoClient
import streamlit_authenticator as stauth
import uuid
from datetime import datetime, timedelta
import bcrypt 

class MongoAuth:
    def __init__(self, connection_string, db_name='streamlit_auth'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.users = self.db['users']
        self.sessions = self.db['sessions']  # Changed from 'cookies' to 'sessions'
        
    def create_user(self, username, email, name, password, preauthorized=False):
        """Create a new user in MongoDB"""
        if self.users.find_one({'username': username}):
            raise Exception('Username already exists')
        
        # Option 1: Using streamlit-authenticator (preferred if installed)
        try:
            hashed_password = stauth.Hasher([password]).generate()[0]
        except:
            # Option 2: Fallback to bcrypt if streamlit-authenticator fails
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_data = {
            'username': username,
            'email': email,
            'name': name,
            'password': hashed_password,
            'preauthorized': preauthorized,
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        
        self.users.insert_one(user_data)
        return True

    def get_user(self, username):
        """Get user by username"""
        return self.users.find_one({'username': username})
    
    def update_user(self, username, update_data):
        """Update user data"""
        result = self.users.update_one(
            {'username': username},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete_user(self, username):
        """Delete a user"""
        result = self.users.delete_one({'username': username})
        return result.deleted_count > 0
    
    def validate_login(self, username, password):
        """Validate user credentials"""
        user = self.get_user(username)
        if not user:
            return False
        
        # Try both verification methods for compatibility
        try:
            # Method 1: streamlit-authenticator
            return stauth.verify_password(password, user['password'])
        except:
            # Method 2: bcrypt fallback
            try:
                return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
            except:
                return False
    
    def create_session(self, username, session_id, expires_at):
        """Create a new session record"""
        session_data = {
            'session_id': session_id,
            'username': username,
            'created_at': datetime.utcnow(),
            'expires_at': expires_at,
            'is_active': True
        }
        
        # Deactivate any existing sessions for this user
        self.sessions.update_many(
            {'username': username},
            {'$set': {'is_active': False}}
        )
        
        self.sessions.insert_one(session_data)
        return True
    
    def validate_session(self, session_id):
        """Validate a session"""
        session = self.sessions.find_one({
            'session_id': session_id,
            'is_active': True,
            'expires_at': {'$gt': datetime.utcnow()}
        })
        
        if session:
            return self.get_user(session['username'])
        return None
    
    def end_session(self, session_id):
        """End a session"""
        result = self.sessions.update_one(
            {'session_id': session_id},
            {'$set': {'is_active': False}}
        )
        return result.modified_count > 0
    
    def cleanup_sessions(self):
        """Clean up expired sessions"""
        result = self.sessions.delete_many({
            'expires_at': {'$lt': datetime.utcnow()}
        })
        return result.deleted_count
    
    def initialize_db(self, admin_username, admin_password, admin_email, admin_name):
        """Initialize database with admin user if empty"""
        if self.users.count_documents({}) == 0:
            return self.create_user(
                username=admin_username,
                email=admin_email,
                name=admin_name,
                password=admin_password,
                preauthorized=True
            )
        return False