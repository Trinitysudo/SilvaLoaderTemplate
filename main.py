from flask import Flask, render_template, request, jsonify, send_from_directory
import secrets
import webview
import json
import os
from api import AuthManager, APIManager
from inject import InjectionManager
from utils import setup_tray

app = Flask(__name__, template_folder='web', static_folder='web')
app.secret_key = secrets.token_hex(16)

# Initialize managers
auth_manager = AuthManager()
injection_manager = InjectionManager()
api_manager = APIManager(auth_manager, injection_manager)

# Window and tray references
window = None
tray_icon = None
is_hidden = False

def show_window():
    """Show the window from tray"""
    global is_hidden
    if window and is_hidden:
        window.show()
        is_hidden = False

def quit_app(icon, item):
    """Quit the application from tray"""
    if icon:
        icon.stop()
    if window:
        window.destroy()

class WindowAPI:
    def minimize_window(self):
        if window:
            window.minimize()
    
    def maximize_window(self):
        if window:
            window.toggle_fullscreen()
    
    def close_window(self):
        if tray_icon:
            tray_icon.stop()
        if window:
            window.destroy()
    
    def hide_to_tray(self):
        """Hide window to system tray"""
        global is_hidden
        if window:
            window.hide()
            is_hidden = True
            return True
        return False
    
    def select_dll_file(self):
        """Open file dialog to select DLL file"""
        if window:
            file_types = ('DLL Files (*.dll)', 'All Files (*.*)')
            result = window.create_file_dialog(webview.OPEN_DIALOG, file_types=file_types)
            if result and len(result) > 0:
                return result[0]
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    result = auth_manager.login(username, password)
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 401

@app.route('/logout', methods=['POST'])
def logout():
    result = auth_manager.logout()
    return jsonify(result)

@app.route('/inject', methods=['POST'])
def inject():
    if not auth_manager.is_authenticated():
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    process_name = data.get('process_name')
    dll_path = data.get('dll_path')
    game_mode = data.get('game_mode', 'fps')
    
    result = injection_manager.inject(process_name=process_name, dll_path=dll_path, game_mode=game_mode)
    return jsonify(result)

@app.route('/api/status')
def status():
    return api_manager.get_status()

@app.route('/premium-features.js')
def serve_premium_js():
    """Serve premium features JavaScript"""
    return send_from_directory('web', 'premium-features.js', mimetype='application/javascript')

@app.route('/api/announcements')
def get_announcements():
    """Get announcements feed"""
    try:
        announcements_path = os.path.join(os.path.dirname(__file__), 'announcements.json')
        with open(announcements_path, 'r') as f:
            announcements = json.load(f)
        return jsonify(announcements)
    except:
        return jsonify([])

@app.route('/api/processes')
def get_processes():
    """Get list of running processes"""
    if not auth_manager.is_authenticated():
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    processes = injection_manager.get_processes()
    return jsonify(processes)

def start_app():
    global window, tray_icon
    window_api = WindowAPI()
    
    # Setup system tray
    tray_icon = setup_tray(window, show_window, quit_app)
    
    # Create frameless window with custom controls - NO DRAGGING
    window = webview.create_window(
        'SilvaLoader',
        app,
        width=1400,
        height=1000,
        frameless=True,
        resizable=False,
        easy_drag=False,
        js_api=window_api
    )
    webview.start(debug=True)

if __name__ == '__main__':
    # For development with Flask dev server:
    # app.run(debug=True, port=5000)
    
    # For production with custom window:
    start_app()
