"""
Silva Loader - Build Script with Obfuscation
Builds an obfuscated standalone EXE
"""

import os
import sys
import shutil
import subprocess

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__', 'dist_obfuscated']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Cleaned {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def install_dependencies():
    """Install required build tools"""
    print_header("INSTALLING BUILD DEPENDENCIES")
    
    dependencies = [
        'pyinstaller',
        'pyarmor',
    ]
    
    for dep in dependencies:
        if not run_command(f'pip install {dep}', f'Installing {dep}'):
            return False
    
    return True

def obfuscate_code():
    """Obfuscate Python source files"""
    print_header("OBFUSCATING SOURCE CODE")
    
    # Create obfuscated directory
    if os.path.exists('dist_obfuscated'):
        shutil.rmtree('dist_obfuscated')
    
    os.makedirs('dist_obfuscated', exist_ok=True)
    
    # List of Python files to obfuscate
    python_files = [
        'main.py',
        'api/auth.py',
        'api/manager.py',
        'api/__init__.py',
        'inject/injection.py',
        'inject/__init__.py',
        'utils/tray.py',
        'utils/__init__.py'
    ]
    
    # Obfuscate each file
    for py_file in python_files:
        if os.path.exists(py_file):
            # Create subdirectories in dist_obfuscated if needed
            output_path = os.path.join('dist_obfuscated', os.path.dirname(py_file))
            os.makedirs(output_path, exist_ok=True)
            
            cmd = f'pyarmor gen -O {output_path} --enable-rft {py_file}'
            if not run_command(cmd, f'Obfuscating {py_file}'):
                print(f"⚠️  Warning: Failed to obfuscate {py_file}, using original")
                shutil.copy(py_file, os.path.join('dist_obfuscated', py_file))
        else:
            print(f"⚠️  {py_file} not found, skipping")
    
    # Copy non-Python files
    print("📁 Copying additional files...")
    
    # Copy web folder
    if os.path.exists('web'):
        shutil.copytree('web', os.path.join('dist_obfuscated', 'web'))
        print("✅ Copied web/")
    
    return True

def create_spec_file():
    """Create PyInstaller spec file"""
    print_header("CREATING PYINSTALLER SPEC FILE")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['dist_obfuscated/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('dist_obfuscated/web', 'web'),
        ('dist_obfuscated/api', 'api'),
        ('dist_obfuscated/inject', 'inject'),
        ('dist_obfuscated/utils', 'utils'),
        ('dist_obfuscated/pyarmor_runtime_000000', 'pyarmor_runtime_000000'),
    ],
    hiddenimports=[
        'flask',
        'webview',
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SilvaLoader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    with open('SilvaLoader.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created SilvaLoader.spec")
    return True

def build_executable():
    """Build the final executable"""
    print_header("BUILDING EXECUTABLE")
    
    # Build with PyInstaller
    cmd = 'pyinstaller --clean --noconfirm SilvaLoader.spec'
    if not run_command(cmd, 'Building with PyInstaller'):
        return False
    
    # Check if EXE was created
    exe_path = os.path.join('dist', 'SilvaLoader.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n✅ Executable created successfully!")
        print(f"📦 Location: {exe_path}")
        print(f"📏 Size: {size_mb:.2f} MB")
        return True
    else:
        print("❌ Executable not found!")
        return False

def create_portable_package():
    """Create a portable package with the executable"""
    print_header("CREATING PORTABLE PACKAGE")
    
    package_name = 'SilvaLoader_Portable'
    package_dir = os.path.join('dist', package_name)
    
    # Create package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executable
    exe_src = os.path.join('dist', 'SilvaLoader.exe')
    exe_dst = os.path.join(package_dir, 'SilvaLoader.exe')
    shutil.copy(exe_src, exe_dst)
    
    # Create README
    readme_content = """SILVA LOADER - PORTABLE EDITION

Installation:
1. Extract all files to a folder
2. Run SilvaLoader.exe
3. Login with your credentials

Default Login (for testing):
- Username: a
- Password: a

Notes:
- No installation required
- All data is stored locally
- Run as Administrator for injection features

For support, visit: [Your Website/Discord]

© 2026 Silva Development
"""
    
    with open(os.path.join(package_dir, 'README.txt'), 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Portable package created: {package_dir}/")
    
    # Create ZIP archive
    try:
        shutil.make_archive(
            os.path.join('dist', package_name),
            'zip',
            os.path.join('dist', package_name)
        )
        print(f"✅ ZIP archive created: dist/{package_name}.zip")
    except Exception as e:
        print(f"⚠️  Failed to create ZIP: {e}")
    
    return True

def main():
    print_header("SILVA LOADER - BUILD SYSTEM")
    print("This script will:")
    print("  1. Install build dependencies")
    print("  2. Obfuscate source code with PyArmor")
    print("  3. Build standalone EXE with PyInstaller")
    print("  4. Create portable package")
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Step 1: Clean
    print_header("CLEANING BUILD DIRECTORIES")
    clean_build_dirs()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies!")
        return False
    
    # Step 3: Obfuscate code
    if not obfuscate_code():
        print("\n❌ Failed to obfuscate code!")
        return False
    
    # Step 4: Create spec file
    if not create_spec_file():
        print("\n❌ Failed to create spec file!")
        return False
    
    # Step 5: Build executable
    if not build_executable():
        print("\n❌ Failed to build executable!")
        return False
    
    # Step 6: Create portable package
    create_portable_package()
    
    # Final summary
    print_header("BUILD COMPLETE!")
    print("✅ Your executable is ready!")
    print("\nOutput files:")
    print("  📦 dist/SilvaLoader.exe - Standalone executable")
    print("  📦 dist/SilvaLoader_Portable/ - Portable folder")
    print("  📦 dist/SilvaLoader_Portable.zip - Portable archive")
    print("\n💡 Tips:")
    print("  - Test the executable before distribution")
    print("  - Consider code signing for production")
    print("  - Check antivirus compatibility")
    print("  - Obfuscated source is in dist_obfuscated/")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n✨ Build successful! ✨")
        else:
            print("\n❌ Build failed!")
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
