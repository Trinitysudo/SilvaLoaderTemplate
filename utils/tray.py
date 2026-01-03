"""
Utils Package - System Tray and Window Management
"""

import pystray
from PIL import Image, ImageDraw
import threading

def create_tray_image():
    """Create a simple icon for the system tray"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple 'S' for Silva
    draw.rectangle([10, 10, 54, 54], fill='white', outline='white')
    draw.rectangle([15, 15, 49, 49], fill='black', outline='black')
    
    return image

def setup_tray(window, show_callback, quit_callback):
    """Setup system tray icon"""
    menu = pystray.Menu(
        pystray.MenuItem('Show Silva Loader', show_callback),
        pystray.MenuItem('Quit', quit_callback)
    )
    
    tray_icon = pystray.Icon(
        'silva_loader',
        create_tray_image(),
        'Silva Loader',
        menu
    )
    
    # Run tray in separate thread
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    
    return tray_icon

__all__ = ['create_tray_image', 'setup_tray']
