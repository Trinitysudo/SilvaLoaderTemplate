from flask import session, jsonify

class AuthManager:
    def __init__(self):
        # Default credentials
        self.users = {
            'a': 'a'
        }
    
    def login(self, username, password):
        """Authenticate user"""
        if username in self.users and self.users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return {'success': True, 'message': 'Login successful'}
        else:
            return {'success': False, 'message': 'Invalid credentials'}
    
    def logout(self):
        """Clear user session"""
        session.clear()
        return {'success': True, 'message': 'Logged out'}
    
    def is_authenticated(self):
        """Check if user is logged in"""
        return session.get('logged_in', False)
    
    def get_username(self):
        """Get current username"""
        return session.get('username', 'Guest')
    
    def add_user(self, username, password):
        """Add a new user"""
        self.users[username] = password
