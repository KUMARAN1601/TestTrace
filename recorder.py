"""
Core recording logic for TestTrace Recorder.
Handles screen capture, global mouse hooks, and keyboard hotkeys.
"""
import os
import json
import time
from datetime import datetime
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PIL import Image
import mss
import mss.tools
from pynput import mouse
import ctypes
from ctypes import wintypes

from session_model import TestSession, TestStep


class Recorder(QObject):
    """Manages test recording with auto-capture and manual triggers."""
    
    step_captured = pyqtSignal(TestStep)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, settings_path: str = "config/settings.json"):
        """
        Initialize recorder with settings.
        
        Args:
            settings_path: Path to settings JSON file
        """
        super().__init__()
        self.settings_path = settings_path
        self.settings = self._load_settings()
        
        self.session: Optional[TestSession] = None
        self.is_recording = False
        self.mouse_listener: Optional[mouse.Listener] = None
        self.session_folder = ""
        self.step_counter = 0
        self.last_capture_time = 0
        
    def _load_settings(self) -> dict:
        """Load settings from JSON file."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Return defaults if file doesn't exist or has errors
        return {
            "output_dir": "./output",
            "auto_capture_on_click": True,
            "capture_delay_ms": 200,
            "highlight_color": "#FF0000",
            "highlight_opacity": 0.3
        }
    
    def start(self, session: TestSession) -> bool:
        """
        Start recording session.
        
        Args:
            session: TestSession instance with metadata
            
        Returns:
            True if recording started successfully
        """
        try:
            self.session = session
            self.is_recording = True
            self.step_counter = 0
            
            # Create session folder for screenshots
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_folder = os.path.join(
                "temp_sessions",
                f"session_{session.session_id}_{timestamp}"
            )
            os.makedirs(self.session_folder, exist_ok=True)
            
            # DISABLED: Auto-capture on click to prevent navigation issues
            # Mouse listener is NOT started - only manual capture available
            # This prevents thread-safety issues and app disappearance
            print("Recording started - Manual capture only (F8 or Highlight button)")
            
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to start recording: {str(e)}")
            self.is_recording = False
            return False
    
    def stop(self) -> Optional[TestSession]:
        """
        Stop recording and return completed session.
        
        Returns:
            Completed TestSession with all captured steps
        """
        self.is_recording = False
        
        # Stop mouse listener
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
            except Exception as e:
                print(f"Warning: Error stopping mouse listener: {e}")
            self.mouse_listener = None
        
        # Set session end time
        if self.session:
            self.session.end_time = datetime.now()
        
        return self.session
    
    def manual_capture(self) -> None:
        """Trigger a manual screenshot capture (hotkey F8)."""
        if self.is_recording:
            self._perform_capture(0, 0, is_manual=True)
    
    def _on_click(self, x: int, y: int, button, pressed: bool) -> None:
        """
        Mouse click event handler.
        
        Args:
            x: Click x coordinate
            y: Click y coordinate
            button: Mouse button pressed
            pressed: True if button pressed, False if released
        """
        # Only capture on left button press
        if not pressed or button != mouse.Button.left:
            return
        
        # Skip if not recording
        if not self.is_recording:
            return
        
        # Apply capture delay to avoid duplicate captures
        current_time = time.time() * 1000  # Convert to ms
        delay = self.settings.get("capture_delay_ms", 200)
        if current_time - self.last_capture_time < delay:
            return
        
        self._perform_capture(x, y, is_manual=False)
    
    def _perform_capture(self, x: int, y: int, is_manual: bool = False) -> None:
        """
        Perform screen capture and create TestStep.
        
        Args:
            x: Click x coordinate (0 if manual)
            y: Click y coordinate (0 if manual)
            is_manual: True if triggered by hotkey, False if auto-capture
        """
        try:
            # Capture screenshot
            screenshot = self._capture_screen()
            if not screenshot:
                self.error_occurred.emit("Failed to capture screenshot")
                return
            
            # Get active window title
            window_title = self._get_active_window_title()
            
            # Increment step counter
            self.step_counter += 1
            
            # Save raw screenshot
            screenshot_filename = f"step_{self.step_counter:03d}.png"
            screenshot_path = os.path.join(self.session_folder, screenshot_filename)
            screenshot.save(screenshot_path)
            
            # Create TestStep object
            step = TestStep(
                step_number=self.step_counter,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                screenshot_path=screenshot_path,
                annotated_path="",  # Will be set after annotation
                highlight_rect={},
                active_window=window_title,
                click_position={"x": x, "y": y} if not is_manual else {},
                description="",
                result="Untested"
            )
            
            # Update last capture time
            self.last_capture_time = time.time() * 1000
            
            # Emit signal with captured step (screenshot PIL Image attached)
            step._raw_image = screenshot  # Temporary attribute for highlighter
            self.step_captured.emit(step)
            
        except Exception as e:
            self.error_occurred.emit(f"Capture error: {str(e)}")
    
    def _capture_screen(self) -> Optional[Image.Image]:
        """
        Capture full screen using mss (supports multi-monitor).
        
        Returns:
            PIL Image of captured screen, or None on failure
        """
        try:
            with mss.mss() as sct:
                # Capture all monitors as one
                monitor = sct.monitors[0]  # Monitor 0 is all monitors combined
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes(
                    'RGB',
                    (screenshot.width, screenshot.height),
                    screenshot.rgb
                )
                return img
                
        except Exception as e:
            print(f"Screenshot capture failed: {e}")
            return None
    
    def _get_active_window_title(self) -> str:
        """
        Get the title of the currently active window (Windows only).
        
        Returns:
            Window title string, or "Unknown" if failed
        """
        try:
            # Windows API calls using ctypes
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return "Unknown"
            
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            
            return buffer.value or "Unknown"
            
        except Exception as e:
            print(f"Failed to get window title: {e}")
            return "Unknown"
