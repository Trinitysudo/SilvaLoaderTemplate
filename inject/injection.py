import psutil
import os
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32process

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
VIRTUAL_MEM = MEM_COMMIT | MEM_RESERVE

class InjectionManager:
    def __init__(self):
        self.last_injection = None
        self.injection_count = 0
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    
    def get_processes(self):
        """Get list of running processes with details"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_info = proc.info
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'path': proc_info['exe'] or 'N/A'
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return sorted(processes, key=lambda x: x['name'].lower())
    
    def inject(self, process_name=None, dll_path=None, game_mode='fps'):
        """Perform DLL injection"""
        if not process_name or not dll_path:
            return {
                'success': False,
                'message': 'Process name and DLL path required'
            }
        
        if not os.path.exists(dll_path):
            return {
                'success': False,
                'message': f'DLL not found: {dll_path}'
            }
        
        try:
            # Find process by name
            target_pid = None
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    target_pid = proc.info['pid']
                    break
            
            if not target_pid:
                return {
                    'success': False,
                    'message': f'Process not found: {process_name}'
                }
            
            # Perform injection
            success = self._inject_dll(target_pid, dll_path)
            
            if success:
                self.injection_count += 1
                self.last_injection = {
                    'process': process_name,
                    'pid': target_pid,
                    'dll': os.path.basename(dll_path),
                    'status': 'injected',
                    'count': self.injection_count,
                    'mode': game_mode
                }
                
                return {
                    'success': True,
                    'message': f'Successfully injected into {process_name}',
                    'details': self.last_injection
                }
            else:
                return {
                    'success': False,
                    'message': 'Injection failed. Check process permissions.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Injection error: {str(e)}'
            }
    
    def _inject_dll(self, pid, dll_path):
        """Inject DLL using LoadLibrary method"""
        try:
            # Get full DLL path
            dll_path = os.path.abspath(dll_path)
            dll_bytes = dll_path.encode('utf-8') + b'\x00'
            dll_len = len(dll_bytes)
            
            # Open process
            h_process = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                pid
            )
            
            if not h_process:
                return False
            
            # Allocate memory in target process
            arg_address = self.kernel32.VirtualAllocEx(
                h_process,
                0,
                dll_len,
                VIRTUAL_MEM,
                PAGE_READWRITE
            )
            
            if not arg_address:
                self.kernel32.CloseHandle(h_process)
                return False
            
            # Write DLL path to allocated memory
            written = ctypes.c_size_t(0)
            self.kernel32.WriteProcessMemory(
                h_process,
                arg_address,
                dll_bytes,
                dll_len,
                ctypes.byref(written)
            )
            
            # Get address of LoadLibraryA
            h_kernel32 = self.kernel32.GetModuleHandleW("kernel32.dll")
            load_library_addr = self.kernel32.GetProcAddress(
                h_kernel32,
                b"LoadLibraryA"
            )
            
            if not load_library_addr:
                self.kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
                self.kernel32.CloseHandle(h_process)
                return False
            
            # Create remote thread
            thread_id = ctypes.c_ulong(0)
            h_thread = self.kernel32.CreateRemoteThread(
                h_process,
                None,
                0,
                load_library_addr,
                arg_address,
                0,
                ctypes.byref(thread_id)
            )
            
            if h_thread:
                # Wait for thread to finish
                self.kernel32.WaitForSingleObject(h_thread, 0xFFFFFFFF)
                self.kernel32.CloseHandle(h_thread)
                
            # Cleanup
            self.kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
            self.kernel32.CloseHandle(h_process)
            
            return True if h_thread else False
            
        except Exception as e:
            print(f"Injection error: {e}")
            return False
    
    def get_status(self):
        """Get injection status"""
        return {
            'last_injection': self.last_injection,
            'total_injections': self.injection_count
        }
