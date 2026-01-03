# 🎮 Silva Loader - Professional Game Loader Template

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A professional, production-ready game loader template with modern UI, obfuscated builds, and comprehensive developer documentation.
THE DDL INJECTION MAY FLAG ANTIVIRUSE Just Delete the FILE if your not using it so if it flags no issue. Its due to it altering memory.
If your just doing Minecraft Injection delete it or let AV, if not you should understand how it works and why it gets flagged, thanks! sorry.

## ✨ Features

- 🎨 **Modern Glass UI** - Custom Aero Glass-themed interface with 8 color themes
- 🔒 **Secure Authentication** - Session-based login system (ready for HWID/key integration)
- 💉 **Injection System** - DLL injection framework (placeholder included)
- 🔧 **Customizable** - Easy rebranding with automated script
- 🛡️ **Obfuscated Builds** - PyArmor + PyInstaller for protected executables
- 📱 **System Tray** - Hide to tray functionality with custom icon
- 🎯 **Clean Architecture** - Organized folder structure for scalability

## 📁 Project Structure

```
SilvaLoader/
├── api/                    # API & Authentication
│   ├── __init__.py
│   ├── auth.py            # User authentication & session management
│   └── manager.py         # API manager & status handling
├── inject/                # Injection System
│   ├── __init__.py
│   └── injection.py       # DLL injection manager
├── utils/                 # Utility Functions
│   ├── __init__.py
│   └── tray.py           # System tray integration
├── web/                   # Frontend
│   └── index.html        # Main GUI (Tailwind + Lucide icons)
├── main.py               # Application entry point
├── build.py              # Build script with obfuscation
├── renamer.py            # Automated rebranding tool
├── requirements.txt      # Python dependencies
├── SETUP_GUIDE.md        # Developer documentation
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Installation

```powershell
# Install dependencies
pip install -r requirements.txt
```

### 2. Run Development Server

```powershell
python main.py
```

**Default Credentials:**
- Username: `a`
- Password: `a`

### 3. Customize Your Loader

Run the automated renamer script:

```powershell
python renamer.py
```

### 4. Build Production Executable

```powershell
python build.py
```

Output: `dist/SilvaLoader.exe`

## 🔧 Configuration

### Authentication System

Edit `api/auth.py`:

```python
class AuthManager:
    def __init__(self):
        self.users = {
            'a': 'a',
            'admin': 'password123'
        }
```

For HWID/key systems, see `SETUP_GUIDE.md`.

### Injection System

Edit `inject/injection.py` to implement real injection.

### UI Themes

8 pre-built color themes available in Settings tab.

## 📚 Documentation

- **SETUP_GUIDE.md** - Developer guide (HWID, keys, injection, API)
- **build.py** - Build system documentation
- **renamer.py** - Rebranding tool

## 🛠️ Architecture

- **Backend:** Flask 3.0.0
- **Frontend:** Tailwind CSS + Lucide Icons
- **Window:** pywebview 5.0.5
- **System Tray:** pystray 0.19.5
- **Build:** PyArmor + PyInstaller


## 📋 Requirements

- **Python:** 3.10+
- **OS:** Windows 10/11
- **Dependencies:** See `requirements.txt`

## 🐛 Troubleshooting

### Build Issues
- **PyArmor not found:** `pip install pyarmor`
- **PyInstaller errors:** `pip install --upgrade pyinstaller`

### Runtime Issues
- **Login not working:** Default is `a` / `a` (check `api/auth.py`)
- **Tray icon missing:** Check Windows system tray settings

## 📝 Credits

**Original Author:** Silva  
**License:** MIT  

---

**Made with ❤️ by Silva**  
*A professional template for game loader developers*
