# 🚀 Silva Loader - Complete Setup Guide for Developers

This template provides a **production-ready loader GUI** with Flask backend that you can customize for your own game cheats, mods, or injectors.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Rebranding Your Loader](#rebranding-your-loader)
3. [HWID Locking System](#hwid-locking-system)
4. [Login & Key System Integration](#login--key-system-integration)
5. [Real Injection Implementation](#real-injection-implementation)
6. [API Server Integration](#api-server-integration)
7. [Production Deployment](#production-deployment)

---

## 🎯 Quick Start

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Run the Loader
```bash
python main.py
```

**Default Login:**
- Username: `a`
- Password: `a`

---

## 🎨 Rebranding Your Loader

### Automated Rebranding

Use the included renamer script to rebrand everything from "Silva" to your brand:

```bash
python renamer.py
```

Follow the prompts to enter your:
- Loader name (e.g., "PhantomLoader")
- Version number
- Discord/Website URL

### Manual Rebranding

If you prefer manual changes, edit these files:

**Frontend (`web/index.html`):**
- Line 295: `<h1>SILVA</h1>` → Your Name
- Line 296: `<p>Loader v1.0.0</p>` → Your Version
- Line 349: `<h2>SILVA</h2>` → Your Name
- Line 451: Title text
- Line 334: Footer text

**Titlebar (`web/index.html`):**
- Line 271: `<div class="titlebar-title">SILVA LOADER v1.0.0</div>`

**Python Files:**
- `main.py`: Window title
- `README.md`: All references

---

## 🔐 HWID Locking System

### Step 1: Create HWID Module

Create `hwid.py`:

```python
import subprocess
import hashlib

class HWIDManager:
    @staticmethod
    def get_hwid():
        """Get unique hardware identifier"""
        try:
            # Get system UUID (motherboard)
            result = subprocess.check_output(
                'wmic csproduct get uuid', 
                shell=True
            ).decode()
            
            uuid = result.split('\n')[1].strip()
            
            # Hash for security
            return hashlib.sha256(uuid.encode()).hexdigest()[:16]
        except:
            return None
    
    @staticmethod
    def validate_hwid(user_hwid, stored_hwid):
        """Check if HWID matches"""
        return user_hwid == stored_hwid
```

### Step 2: Update Auth Manager

In `auth.py`, add HWID checking:

```python
from hwid import HWIDManager

class AuthManager:
    def __init__(self):
        self.users = {
            'username': {
                'password': 'password123',
                'hwid': 'abc123def456',  # Store allowed HWID
                'subscription': 'lifetime'
            }
        }
    
    def login(self, username, password):
        if username not in self.users:
            return {'success': False, 'message': 'Invalid credentials'}
        
        user = self.users[username]
        
        # Check password
        if user['password'] != password:
            return {'success': False, 'message': 'Invalid credentials'}
        
        # Check HWID
        current_hwid = HWIDManager.get_hwid()
        if not HWIDManager.validate_hwid(current_hwid, user['hwid']):
            return {'success': False, 'message': 'HWID Mismatch! Contact support.'}
        
        session['logged_in'] = True
        session['username'] = username
        session['hwid'] = current_hwid
        
        return {'success': True, 'message': 'Login successful'}
```

### Step 3: Display HWID in Settings

Add HWID display to settings tab:

```html
<div class="bg-white/5 p-4 rounded-xl border border-white/5">
    <p class="text-xs text-gray-400 mb-2">Your HWID</p>
    <p id="hwid-display" class="text-sm font-mono text-white"></p>
    <button onclick="copyHWID()" class="mt-2 text-xs text-gray-400 hover:text-white">
        Copy HWID
    </button>
</div>
```

JavaScript:
```javascript
// Get and display HWID
fetch('/api/hwid')
    .then(r => r.json())
    .then(data => {
        document.getElementById('hwid-display').textContent = data.hwid;
    });

function copyHWID() {
    const hwid = document.getElementById('hwid-display').textContent;
    navigator.clipboard.writeText(hwid);
    alert('HWID copied to clipboard!');
}
```

---

## 🔑 Login & Key System Integration

### Option 1: Database-Based System

#### Setup Database

```python
# database.py
import sqlite3
import hashlib
from datetime import datetime, timedelta

class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                hwid TEXT,
                license_key TEXT,
                expiry_date TEXT,
                subscription_type TEXT,
                created_at TEXT
            )
        ''')
        self.conn.commit()
    
    def add_user(self, username, password, license_key, days=30):
        cursor = self.conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        expiry = (datetime.now() + timedelta(days=days)).isoformat()
        
        cursor.execute('''
            INSERT INTO users (username, password_hash, license_key, expiry_date, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, license_key, expiry, datetime.now().isoformat()))
        
        self.conn.commit()
    
    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        return cursor.fetchone()
    
    def check_subscription(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT expiry_date FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            expiry = datetime.fromisoformat(result[0])
            return expiry > datetime.now()
        return False
```

#### Update Auth Manager

```python
from database import UserDatabase

class AuthManager:
    def __init__(self):
        self.db = UserDatabase()
    
    def login(self, username, password):
        # Verify credentials
        user = self.db.verify_user(username, password)
        if not user:
            return {'success': False, 'message': 'Invalid credentials'}
        
        # Check subscription
        if not self.db.check_subscription(username):
            return {'success': False, 'message': 'Subscription expired'}
        
        # Check HWID (optional)
        from hwid import HWIDManager
        current_hwid = HWIDManager.get_hwid()
        
        session['logged_in'] = True
        session['username'] = username
        
        return {'success': True, 'message': 'Login successful'}
```

### Option 2: API-Based Key System

```python
# keyauth.py
import requests

class KeyAuthManager:
    def __init__(self, api_url, app_id, app_secret):
        self.api_url = api_url
        self.app_id = app_id
        self.app_secret = app_secret
    
    def validate_license(self, license_key, hwid):
        """Validate license with your API"""
        try:
            response = requests.post(f'{self.api_url}/validate', json={
                'app_id': self.app_id,
                'app_secret': self.app_secret,
                'license_key': license_key,
                'hwid': hwid
            }, timeout=5)
            
            data = response.json()
            return {
                'valid': data.get('valid', False),
                'username': data.get('username'),
                'expiry': data.get('expiry'),
                'subscription': data.get('subscription_type')
            }
        except:
            return {'valid': False, 'message': 'API unreachable'}
```

Usage in `auth.py`:
```python
from keyauth import KeyAuthManager
from hwid import HWIDManager

class AuthManager:
    def __init__(self):
        self.key_auth = KeyAuthManager(
            api_url='https://your-api.com',
            app_id='your_app_id',
            app_secret='your_secret'
        )
    
    def login_with_key(self, license_key):
        hwid = HWIDManager.get_hwid()
        result = self.key_auth.validate_license(license_key, hwid)
        
        if result['valid']:
            session['logged_in'] = True
            session['username'] = result['username']
            return {'success': True}
        else:
            return {'success': False, 'message': 'Invalid license'}
```

---

## 💉 Real Injection Implementation

### Step 1: Process Injection Module

Create `injector.py`:

```python
import ctypes
import sys
from ctypes import wintypes
import os

class ProcessInjector:
    def __init__(self):
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        
    def find_process(self, process_name):
        """Find process by name"""
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                return proc.info['pid']
        return None
    
    def inject_dll(self, pid, dll_path):
        """Inject DLL into target process"""
        if not os.path.exists(dll_path):
            return {'success': False, 'message': 'DLL not found'}
        
        try:
            # Get full path
            dll_path = os.path.abspath(dll_path)
            
            # Open process
            PROCESS_ALL_ACCESS = 0x1F0FFF
            h_process = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS, False, pid
            )
            
            if not h_process:
                return {'success': False, 'message': 'Failed to open process'}
            
            # Allocate memory in target process
            dll_path_bytes = dll_path.encode('utf-8') + b'\x00'
            arg_address = self.kernel32.VirtualAllocEx(
                h_process, 0, len(dll_path_bytes),
                0x3000, 0x40  # MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE
            )
            
            # Write DLL path to allocated memory
            written = ctypes.c_size_t(0)
            self.kernel32.WriteProcessMemory(
                h_process, arg_address,
                dll_path_bytes, len(dll_path_bytes),
                ctypes.byref(written)
            )
            
            # Get LoadLibraryA address
            h_kernel32 = self.kernel32.GetModuleHandleW('kernel32.dll')
            load_library_addr = self.kernel32.GetProcAddress(
                h_kernel32, b'LoadLibraryA'
            )
            
            # Create remote thread
            thread_id = ctypes.c_ulong(0)
            h_thread = self.kernel32.CreateRemoteThread(
                h_process, None, 0,
                load_library_addr, arg_address,
                0, ctypes.byref(thread_id)
            )
            
            if h_thread:
                self.kernel32.WaitForSingleObject(h_thread, 0xFFFFFFFF)
                self.kernel32.CloseHandle(h_thread)
                self.kernel32.CloseHandle(h_process)
                
                return {
                    'success': True,
                    'message': 'Injection successful',
                    'pid': pid,
                    'dll': dll_path
                }
            else:
                return {'success': False, 'message': 'Failed to create thread'}
                
        except Exception as e:
            return {'success': False, 'message': str(e)}
```

### Step 2: Update Injection Manager

In `injection.py`:

```python
from injector import ProcessInjector
import os

class InjectionManager:
    def __init__(self):
        self.injector = ProcessInjector()
        self.last_injection = None
        self.injection_count = 0
        
        # Configure your DLL path and target process
        self.dll_path = os.path.join(os.getcwd(), 'your_cheat.dll')
        self.target_process = 'csgo.exe'  # Change to your target
    
    def inject(self):
        """Perform actual DLL injection"""
        # Find target process
        pid = self.injector.find_process(self.target_process)
        
        if not pid:
            return {
                'success': False,
                'message': f'{self.target_process} not found! Please launch the game first.'
            }
        
        # Check if DLL exists
        if not os.path.exists(self.dll_path):
            return {
                'success': False,
                'message': 'DLL file not found! Please reinstall.'
            }
        
        # Inject
        result = self.injector.inject_dll(pid, self.dll_path)
        
        if result['success']:
            self.injection_count += 1
            self.last_injection = {
                'process': self.target_process,
                'pid': pid,
                'status': 'injected',
                'count': self.injection_count
            }
        
        return result
```

### Step 3: Add Process Detection

Add to `web/index.html`:

```javascript
// Check if game is running before inject
async function checkGameRunning() {
    const response = await fetch('/api/check-process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process: 'csgo.exe' })
    });
    
    const data = await response.json();
    return data.running;
}

// Update inject button click
injectBtn.addEventListener('click', async () => {
    if (isInjecting) return;
    
    // Check if game is running
    const isRunning = await checkGameRunning();
    if (!isRunning) {
        injectText.textContent = "GAME NOT FOUND";
        setTimeout(() => {
            injectText.textContent = "INJECT";
        }, 2000);
        return;
    }
    
    // Continue with injection...
});
```

Add endpoint to `main.py`:

```python
@app.route('/api/check-process', methods=['POST'])
def check_process():
    data = request.json
    process_name = data.get('process')
    
    pid = injection_manager.injector.find_process(process_name)
    return jsonify({'running': pid is not None, 'pid': pid})
```

---

## 🌐 API Server Integration

### Using Your Own Backend

Replace the local Flask server with API calls:

```javascript
// In web/index.html
const API_URL = 'https://your-api-server.com';

// Login
async function login(username, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (data.token) {
        localStorage.setItem('auth_token', data.token);
        return { success: true };
    }
    
    return { success: false, message: data.message };
}

// Inject with auth
async function performInject() {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(`${API_URL}/inject/request`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}
```

---

## 📦 Production Deployment

### Building Executable

Use **PyInstaller** to create standalone EXE:

```bash
pip install pyinstaller

# Create single EXE
pyinstaller --onefile --windowed --icon=icon.ico main.py

# With additional files
pyinstaller --onefile --windowed \
    --add-data "web;web" \
    --add-data "your_cheat.dll;." \
    --icon=icon.ico \
    main.py
```

### Obfuscation

Protect your code with **PyArmor**:

```bash
pip install pyarmor

# Obfuscate all Python files
pyarmor gen main.py auth.py injection.py LoginManager.py hwid.py
```

### Code Signing (Optional)

Sign your EXE to avoid Windows SmartScreen:

1. Get code signing certificate
2. Use `signtool.exe`:
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com main.exe
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. Injection Fails**
- Run as Administrator
- Disable antivirus temporarily
- Check if process name is correct
- Verify DLL is compiled for correct architecture (x86/x64)

**2. Window Not Showing**
- Check if `pywebview` is installed correctly
- Try running Flask dev server: `app.run(debug=True, port=5000)`

**3. HWID Changes**
- HWID can change after hardware changes
- Implement HWID reset system in your backend

**4. Database Locked**
- Use `check_same_thread=False` in SQLite connection
- Consider using PostgreSQL for production

---

## 📚 Additional Resources

- **Injection Techniques:** Research DLL injection, manual mapping, process hollowing
- **Anti-Cheat Bypass:** Study game-specific protections
- **Backend APIs:** KeyAuth, Auth.gg, custom solutions
- **Python Obfuscation:** PyArmor, Cython compilation

---

## ⚠️ Legal Disclaimer

This template is for **educational purposes only**. Creating game cheats or injectors may violate:
- Game Terms of Service
- Anti-cheat software agreements
- Local laws and regulations

**Use responsibly and only on software you own or have permission to modify.**

---

## 💬 Support

For questions about this template:
1. Check documentation thoroughly
2. Review the code comments
3. Test with simple DLL first

**Silva Credits:** Original template creator - do not remove from credits tab.

---

## 🎉 Final Notes

This template provides everything you need:
- ✅ Professional UI with animations
- ✅ Theme customization
- ✅ Session management
- ✅ System tray support
- ✅ Modular architecture
- ✅ Production-ready structure

**Good luck with your project!** 🚀
