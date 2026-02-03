import time
import threading
from typing import Optional, Callable
import pygetwindow as gw
import psutil


class WindowMonitor:
    """Monitors active window changes and triggers callbacks."""
    
    def __init__(self, callback: Callable[[str, Optional[str]], None]):
        self.callback = callback
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.last_process: Optional[str] = None
        self.last_title: Optional[str] = None
        self.poll_interval = 0.5  # Check every 500ms
    
    def start(self):
        """Start monitoring window changes."""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop(self):
        """Stop monitoring window changes."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                active_window = self._get_active_window_info()
                if active_window:
                    process_name, window_title = active_window
                    
                    # Only trigger callback if window changed
                    if (process_name != self.last_process or 
                        window_title != self.last_title):
                        self.last_process = process_name
                        self.last_title = window_title
                        self.callback(process_name, window_title)
                        
            except Exception:
                pass
            
            time.sleep(self.poll_interval)
    
    def _get_active_window_info(self) -> Optional[tuple]:
        """Get the currently active window's process name and title."""
        try:
            # Get active window
            active_window = gw.getActiveWindow()
            if not active_window:
                return None
            
            window_title = active_window.title
            
            # Get process name from window handle
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            # Get window thread process ID
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(active_window._hWnd, ctypes.byref(pid))
            
            # Ignore our own process to avoid feedback loops
            import os
            if pid.value == os.getpid():
                return None
            
            # Get process name
            try:
                process = psutil.Process(pid.value)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None
            
            return (process_name, window_title if window_title else None)
            
        except Exception:
            return None
    
    def get_current_window(self) -> Optional[tuple]:
        """Get current window info without monitoring."""
        return self._get_active_window_info()
