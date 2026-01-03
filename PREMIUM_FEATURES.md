# Silva Loader - Premium Features Guide

## 🎉 What's New

Your Silva Loader now includes **premium features** for professional DLL injection:

### ✨ New Features

1. **📢 Announcements Feed** - Real-time news and updates on the dashboard
2. **🎮 Game Mode Selection** - Choose between Minecraft or FPS mode
3. **🎯 Process Selector** - Beautiful modal with all running processes
4. **📁 DLL File Picker** - Easy DLL selection with gear icon
5. **💉 Real Injection** - Working DLL injection using Windows API
6. **🧪 Test DLL Included** - TestDLL.cpp for testing with Notepad

---

## 🚀 Quick Start Guide

### 1. Install New Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `psutil` - For process enumeration
- `pywin32` - For Windows API injection

### 2. Build the Test DLL

**Option A: Using Visual Studio**

1. Open "Developer Command Prompt for VS 2019/2022"
2. Navigate to Silva Loader directory
3. Run: `build_dll.bat`

**Option B: Manual Compilation**

```cmd
cl /LD /O2 TestDLL.cpp user32.lib /Fe:TestDLL.dll
```

This creates `TestDLL.dll` which displays a message box when injected.

### 3. Test the Injection

1. Open Notepad (notepad.exe)
2. Run Silva Loader: `python main.py`
3. Login with `a` / `a`
4. Click **"FPS GAMES"** mode
5. Select **notepad.exe** from the process list
6. Click the **gear icon** ⚙️
7. Enter DLL path: `C:\Users\...\SilvaLoader\TestDLL.dll`
8. Click **"INJECT NOW"**
9. See the message box appear in Notepad! 💥

---

## 📋 Feature Walkthrough

### Announcements Feed

Located at the top of the Dashboard tab:

- **Auto-loads** on startup from `announcements.json`
- Color-coded by type (info/success/warning)
- Icons for visual appeal
- Scrollable if many announcements

**Customize:**

Edit `announcements.json`:

```json
{
    "title": "Your Announcement",
    "message": "Your message here",
    "type": "success",
    "date": "2026-01-03",
    "icon": "rocket"
}
```

**Icons:** rocket, crosshair, crown, shield-alert, info, bell

### Game Mode Selection

Two modes available:

#### 🟢 Minecraft Mode
- Auto-injection (when implemented)
- Detects Minecraft Java Edition
- One-click inject

#### 🔫 FPS Mode
- Manual process selection
- Works with any game
- Full control over injection

### Process Selector

**Features:**
- 🔍 **Search bar** - Filter processes by name
- 📊 **Live process list** - All running processes
- 🎨 **Icons** - Process icons with themed colors
- 📍 **PID display** - Process ID for each process
- ⚡ **Fast selection** - Click to select instantly

**How it works:**
1. Click "FPS GAMES"
2. Modal appears with all processes
3. Search or scroll to find your game
4. Click the process to select it
5. Modal closes automatically

### DLL File Picker

After selecting a process:

1. **Gear icon** appears (⚙️)
2. Click it to open file selection
3. Enter full DLL path
4. DLL info displays
5. Inject button activates

**Supported Paths:**
- `C:\Full\Path\To\YourDLL.dll`
- Relative paths (from loader directory)
- Network paths (if accessible)

### Real Injection System

**Technical Details:**

- **Method:** LoadLibrary injection via CreateRemoteThread
- **Privileges:** Requires admin for protected processes
- **Architecture:** Supports x86 and x64 (must match target)
- **Safety:** Validates DLL exists before injection

**Injection Flow:**

1. ✅ Validates DLL file exists
2. 🔍 Finds target process by name
3. 🔓 Opens process with PROCESS_ALL_ACCESS
4. 💾 Allocates memory in target process
5. ✍️ Writes DLL path to allocated memory
6. 🚀 Creates remote thread with LoadLibraryA
7. ⏳ Waits for thread completion
8. 🧹 Cleans up allocated memory

**Error Handling:**
- Process not found
- DLL file missing
- Access denied (need admin)
- Injection failed (incompatible DLL)

---

## 🛡️ Running with Admin Rights

For injecting into protected processes:

**Windows 10/11:**

1. Right-click `main.py`
2. Select "Run as administrator"

**OR**

Create shortcut with admin privilege:
1. Right-click Python shortcut
2. Properties → Advanced
3. Check "Run as administrator"

---

## 🧪 Testing Guide

### Test 1: Basic Injection (Notepad)

```
Target: notepad.exe
DLL: TestDLL.dll
Expected: Message box appears
```

1. Open Notepad
2. Select FPS mode
3. Choose notepad.exe
4. Select TestDLL.dll
5. Click INJECT NOW
6. ✅ Message box: "Silva Loader - DLL Successfully Injected!"

### Test 2: Process Not Found

```
Target: nonexistent.exe
Expected: Error message
```

### Test 3: Invalid DLL Path

```
DLL: C:\fake\path\dll.dll
Expected: "DLL not found" error
```

### Test 4: Permission Denied

```
Target: System process (e.g., csrss.exe)
Expected: Access denied or injection failed
```

---

## 🔧 Troubleshooting

### "Process not found"
- ✅ Ensure target process is running
- ✅ Check process name spelling
- ✅ Refresh process list

### "DLL not found"
- ✅ Verify full DLL path is correct
- ✅ Check file exists at that location
- ✅ Use absolute paths, not relative

### "Access Denied" / "Injection failed"
- ✅ Run Silva Loader as Administrator
- ✅ Disable antivirus temporarily
- ✅ Check if process is protected

### "Injection failed. Check process permissions"
- ✅ Target might be 64-bit (need 64-bit DLL)
- ✅ Target might be protected by anti-cheat
- ✅ DLL architecture mismatch

### Message box doesn't appear
- ✅ DLL was injected but DllMain didn't execute
- ✅ Check Windows Event Viewer for errors
- ✅ Recompile DLL with debug output

---

## 🏗️ Creating Your Own DLL

### Basic Template

```cpp
#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID lpReserved) {
    switch (reason) {
        case DLL_PROCESS_ATTACH:
            // Your code here - runs when injected
            MessageBoxA(NULL, "Injected!", "Success", MB_OK);
            break;
    }
    return TRUE;
}
```

### Compile

```cmd
cl /LD your_dll.cpp user32.lib /Fe:your_dll.dll
```

### Advanced Features

```cpp
// Create a thread for continuous execution
CreateThread(NULL, 0, YourThreadFunc, NULL, 0, NULL);

// Hook functions
#include "MinHook.h"  // Popular hooking library

// Read/Write process memory
ReadProcessMemory(...);
WriteProcessMemory(...);
```

---

## 🎨 Customizing Announcements

Edit `announcements.json`:

```json
[
    {
        "id": 1,
        "title": "Custom Title",
        "message": "Your custom message goes here",
        "type": "success",
        "date": "2026-01-03",
        "icon": "rocket"
    }
]
```

**Types:** `info`, `success`, `warning`, `error`  
**Icons:** `rocket`, `crosshair`, `crown`, `shield-alert`, `info`, `bell`

---

## 📊 API Endpoints

### GET /api/announcements
Returns announcements JSON array

### GET /api/processes
Returns list of running processes
```json
[
    {
        "pid": 1234,
        "name": "notepad.exe",
        "path": "C:\\Windows\\System32\\notepad.exe"
    }
]
```

### POST /inject
Injects DLL into process
```json
{
    "process_name": "notepad.exe",
    "dll_path": "C:\\TestDLL.dll",
    "game_mode": "fps"
}
```

---

## 🔐 Security Notes

- DLL injection requires Administrator privileges for most processes
- Some games have anti-cheat that detects injection
- Always use trusted DLLs only
- Test on safe applications first (Notepad, Calculator)
- Backup important data before testing
- Silva Loader is for educational purposes

---

## 🐛 Known Issues

1. **64-bit vs 32-bit mismatch** - Ensure DLL architecture matches target
2. **Protected processes** - Cannot inject into system-protected processes
3. **Anti-cheat detection** - Some games will detect and ban
4. **File path backslashes** - Use double backslashes in paths: `C:\\path\\to\\dll.dll`

---

## 🎯 Next Steps

1. ✅ Test with Notepad + TestDLL
2. ⚙️ Build your custom DLL
3. 🎮 Test with your target game
4. 🛡️ Implement anti-detection if needed
5. 📦 Distribute using `build.py`

---

## 📞 Support

For issues:
- Check `SETUP_GUIDE.md` for developer info
- Review error messages in console
- Test with TestDLL first
- Ensure admin privileges

---

**Made with ❤️ by Silva**  
*Premium DLL Injection - Now Production Ready*
