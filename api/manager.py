from flask import jsonify, session
import time
import socket

class APIManager:
    def __init__(self, auth_manager, injection_manager):
        self.auth = auth_manager
        self.injection = injection_manager
        self.ping_start = time.time()
    
    def get_ping(self):
        """Calculate real ping to server"""
        try:
            start = time.time()
            # Ping localhost (can be changed to your API server)
            socket.create_connection(('127.0.0.1', 5000), timeout=1)
            end = time.time()
            ping_ms = int((end - start) * 1000)
            return f"{ping_ms}ms"
        except:
            return "--ms"
    
    def get_status(self):
        """Get user and system status"""
        if not self.auth.is_authenticated():
            return jsonify({'authenticated': False})
        
        return jsonify({
            'authenticated': True,
            'username': self.auth.get_username(),
            'version': '1.0.0',
            'ping': self.get_ping(),
            'subscription': 'LIFETIME',
            'hwid': 'MATCHED',
            'injection_status': self.injection.get_status()
        })
