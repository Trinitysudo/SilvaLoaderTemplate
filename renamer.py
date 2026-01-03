"""
Silva Loader - Automatic Rebranding Script
Renames all instances of "Silva" to your brand name (except in credits)
"""

import os
import re

def rebrand_loader():
    print("=" * 60)
    print("  SILVA LOADER - REBRANDING TOOL")
    print("=" * 60)
    print("\nThis script will rename your loader from 'Silva' to your brand.")
    print("Credits to Silva will be preserved.\n")
    
    # Get user inputs
    new_name = input("Enter your loader name (e.g., PhantomLoader): ").strip()
    if not new_name:
        print("❌ Name cannot be empty!")
        return
    
    new_version = input("Enter version (default: 1.0.0): ").strip() or "1.0.0"
    new_url = input("Enter your website/Discord URL (optional): ").strip()
    
    print(f"\n🎨 Rebranding to: {new_name} v{new_version}")
    print("⏳ Processing files...\n")
    
    # Files to rebrand
    files_to_update = {
        'web/index.html': rebrand_html,
        'main.py': rebrand_python,
        'README.md': rebrand_readme,
    }
    
    changes_made = 0
    
    for file_path, rebrand_func in files_to_update.items():
        if os.path.exists(file_path):
            try:
                count = rebrand_func(file_path, new_name, new_version, new_url)
                changes_made += count
                print(f"✅ {file_path} - {count} changes")
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")
        else:
            print(f"⚠️  {file_path} - File not found")
    
    print(f"\n🎉 Rebranding complete! {changes_made} total changes made.")
    print(f"\n📝 Your loader is now: {new_name}")
    print("⚠️  Remember to update icon.ico and create your own logo!")
    print("\n💡 Tip: Check the SETUP_GUIDE.md for next steps.")

def rebrand_html(file_path, new_name, new_version, new_url):
    """Rebrand HTML file - preserve credits section"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    # Split content to preserve credits
    if '<!-- CREDITS TAB -->' in content:
        parts = content.split('<!-- CREDITS TAB -->')
        main_content = parts[0]
        credits_content = '<!-- CREDITS TAB -->' + parts[1]
        
        # Rebrand main content only
        main_content = main_content.replace('SILVA', new_name.upper())
        main_content = main_content.replace('Silva', new_name)
        main_content = main_content.replace('silva', new_name.lower())
        
        # Update version
        main_content = re.sub(r'v\d+\.\d+\.\d+', f'v{new_version}', main_content)
        main_content = re.sub(r'Loader v\d+\.\d+\.\d+', f'Loader v{new_version}', main_content)
        
        # Update titlebar
        main_content = re.sub(
            r'SILVA LOADER v\d+\.\d+\.\d+',
            f'{new_name.upper()} LOADER v{new_version}',
            main_content
        )
        
        # Update footer
        if new_url:
            main_content = re.sub(
                r'SILVA NETWORKS // ENCRYPTED',
                f'{new_name.upper()} // {new_url}',
                main_content
            )
        else:
            main_content = re.sub(
                r'SILVA NETWORKS // ENCRYPTED',
                f'{new_name.upper()} // ENCRYPTED',
                main_content
            )
        
        # Recombine
        content = main_content + credits_content
        
        # Count changes
        changes = len([i for i in range(len(original)) if i < len(content) and original[i] != content[i]])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes // 10  # Approximate number of actual replacements

def rebrand_python(file_path, new_name, new_version, new_url):
    """Rebrand Python files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_length = len(content)
    
    # Replace window title
    content = re.sub(
        r"'SilvaLoader'",
        f"'{new_name}'",
        content
    )
    
    # Replace comments
    content = content.replace('Silva Loader', f'{new_name}')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return 1 if len(content) != original_length else 0

def rebrand_readme(file_path, new_name, new_version, new_url):
    """Rebrand README but preserve credits"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_length = len(content)
    
    # Replace title
    content = re.sub(r'# SilvaLoader.*', f'# {new_name} - Flask Backend', content)
    
    # Replace descriptions (but not in credits section)
    lines = content.split('\n')
    new_lines = []
    in_credits = False
    
    for line in lines:
        if 'credit' in line.lower() or 'silva' in line.lower() and 'by' in line.lower():
            in_credits = True
        
        if not in_credits:
            line = line.replace('SilvaLoader', new_name)
            line = line.replace('Silva Loader', new_name)
            line = re.sub(r'v\d+\.\d+\.\d+', f'v{new_version}', line)
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return 1 if len(content) != original_length else 0

def create_config():
    """Create a config file with the new branding"""
    config = {
        'loader_name': '',
        'version': '',
        'author': '',
        'url': ''
    }
    
    # Would save this to config.json for future reference

if __name__ == '__main__':
    try:
        rebrand_loader()
        input("\n\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n❌ Rebranding cancelled.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        input("\nPress Enter to exit...")
