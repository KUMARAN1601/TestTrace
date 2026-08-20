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
from PIL import Image, ImageDraw
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
    click_detected = pyqtSignal(int, int)  # Thread-safe signal for mouse clicks (x, y)
    
    def __init__(self, settings_path: str = "config/settings.json", base_dir: str = None):
        """
        Initialize recorder with settings.
        
        Args:
            settings_path: Path to settings JSON file
            base_dir: Base directory for the application (for .exe support)
        """
        super().__init__()
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.settings_path = settings_path if os.path.isabs(settings_path) else os.path.join(self.base_dir, settings_path)
        self.settings = self._load_settings()
        
        self.session: Optional[TestSession] = None
        self.is_recording = False
        self.mouse_listener: Optional[mouse.Listener] = None
        self.listener_paused = False  # Flag to pause listener during UI actions
        self.session_folder = ""
        self.step_counter = 0
        self.last_capture_time = 0
        self.cursor_image = self._create_cursor_image()
        self.control_panel_rect = None  # Will store control panel bounds
        
        # Connect click signal to handler (thread-safe bridge)
        self.click_detected.connect(self._handle_click_on_main_thread)
    
    def pause_listener(self) -> None:
        """Pause the mouse listener temporarily (e.g., during UI interactions)."""
        self.listener_paused = True
        print("Mouse listener paused")
    
    def resume_listener(self) -> None:
        """Resume the mouse listener after being paused."""
        self.listener_paused = False
        print("Mouse listener resumed")
    
    def set_control_panel_rect(self, x: int, y: int, width: int, height: int) -> None:
        """
        Set the control panel bounding box for click filtering.
        
        Args:
            x: Control panel x position
            y: Control panel y position
            width: Control panel width
            height: Control panel height
        """
        self.control_panel_rect = (x, y, width, height)
        print(f"Control panel bounds set: ({x}, {y}, {width}, {height})")
        
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
            
            # Create session folder for screenshots in local temp_sessions
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_folder = os.path.join(
                self.base_dir,
                "temp_sessions",
                f"session_{session.session_id}_{timestamp}"
            )
            os.makedirs(self.session_folder, exist_ok=True)
            
            # Start mouse listener for auto-capture on click (SILENT MODE)
            if self.settings.get("auto_capture_on_click", True):
                try:
                    self.mouse_listener = mouse.Listener(on_click=self._on_click)
                    self.mouse_listener.start()
                    print("Recording started - Silent auto-capture enabled")
                except Exception as e:
                    print(f"Warning: Failed to start mouse listener: {e}")
                    print("Recording started - Manual capture only (F8 or Highlight button)")
            else:
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
        Mouse click event handler (runs in pynput thread).
        Emits thread-safe signal to main thread.
        
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
        
        # Skip if listener is paused (during UI interactions)
        if self.listener_paused:
            return
        
        # Filter out clicks on control panel
        if self.control_panel_rect is not None:
            cp_x, cp_y, cp_w, cp_h = self.control_panel_rect
            if cp_x <= x <= cp_x + cp_w and cp_y <= y <= cp_y + cp_h:
                print(f"Ignored click on control panel at ({x}, {y})")
                return
        
        # Apply capture delay to avoid duplicate captures
        current_time = time.time() * 1000  # Convert to ms
        delay = self.settings.get("capture_delay_ms", 200)
        if current_time - self.last_capture_time < delay:
            return
        
        # Emit signal to main thread (THREAD-SAFE)
        self.click_detected.emit(x, y)
    
    def _handle_click_on_main_thread(self, x: int, y: int) -> None:
        """
        Handle click event on main GUI thread (SILENT - NO POPUPS).
        
        Args:
            x: Click x coordinate
            y: Click y coordinate
        """
        self._perform_capture(x, y, is_manual=False, silent=True)
    
    def _perform_capture(self, x: int, y: int, is_manual: bool = False, silent: bool = False) -> None:
        """
        Perform screen capture and create TestStep.
        
        Args:
            x: Click x coordinate (0 if manual)
            y: Click y coordinate (0 if manual)
            is_manual: True if triggered by hotkey, False if auto-capture
            silent: True for silent auto-capture (no step emission to highlighter)
        """
        try:
            # Capture screenshot
            screenshot = self._capture_screen()
            if not screenshot:
                if not silent:
                    self.error_occurred.emit("Failed to capture screenshot")
                return
            
            # Overlay cursor for auto-capture clicks
            if not is_manual and x > 0 and y > 0:
                screenshot = self._overlay_cursor(screenshot, x, y)
            
            # Get active window title
            window_title = self._get_active_window_title()
            
            # Increment step counter
            self.step_counter += 1
            
            # Save screenshot with cursor overlay
            screenshot_filename = f"step_{self.step_counter:03d}.png"
            screenshot_path = os.path.join(self.session_folder, screenshot_filename)
            screenshot.save(screenshot_path)
            
            # For auto-capture: also save as annotated (no additional annotation needed)
            if not is_manual and silent:
                annotated_filename = f"step_{self.step_counter:03d}_annotated.png"
                annotated_path = os.path.join(self.session_folder, annotated_filename)
                screenshot.save(annotated_path)
            else:
                annotated_path = ""
            
            # Create TestStep object
            step = TestStep(
                step_number=self.step_counter,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                screenshot_path=screenshot_path,
                annotated_path=annotated_path,  # Auto-capture has annotated path immediately
                highlight_rect={},
                active_window=window_title,
                click_position={"x": x, "y": y} if not is_manual else {},
                description=f"Mouse Click at ({x}, {y})" if silent else "",
                result="Pass" if silent else "Untested"
            )
            
            # Update last capture time
            self.last_capture_time = time.time() * 1000
            
            if silent:
                # SILENT MODE: Add step directly to session (NO POPUP, NO HIGHLIGHTER)
                if self.session:
                    self.session.add_step(step)
                    print(f"✓ Auto-captured: Step {self.step_counter} at ({x}, {y})")
                    print(f"  Window: {window_title}")
                    print(f"  Total steps in session: {len(self.session.steps)}")
                else:
                    print(f"ERROR: No active session to add step to!")
            else:
                # MANUAL MODE: Emit signal to show highlighter for annotation
                step._raw_image = screenshot  # Temporary attribute for highlighter
                self.step_captured.emit(step)
            
        except Exception as e:
            if not silent:
                self.error_occurred.emit(f"Capture error: {str(e)}")
            else:
                print(f"Auto-capture error: {e}")
    
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
    
    def _create_cursor_image(self) -> Image.Image:
        """
        Create a simple mouse cursor arrow image.
        
        Returns:
            PIL Image of cursor (transparent background)
        """
        try:
            # Create a 24x24 transparent image for cursor
            cursor = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
            draw = ImageDraw.Draw(cursor)
            
            # Draw a simple white arrow pointer with black outline
            arrow_points = [
                (4, 4),   # Top
                (4, 18),  # Bottom of shaft
                (8, 14),  # Inner bottom left
                (12, 20), # Outer point
                (14, 18), # Inner point
                (10, 12), # Inner top right
                (18, 12), # Outer right
                (4, 4)    # Back to top
            ]
            
            # Draw black outline
            draw.polygon(arrow_points, fill=(0, 0, 0, 255), outline=(0, 0, 0, 255))
            
            # Draw white fill (slightly smaller)
            arrow_fill = [
                (5, 5),
                (5, 17),
                (8, 14),
                (11, 19),
                (13, 17),
                (10, 12),
                (17, 12),
                (5, 5)
            ]
            draw.polygon(arrow_fill, fill=(255, 255, 255, 255))
            
            return cursor
            
        except Exception as e:
            print(f"Failed to create cursor image: {e}")
            # Return a simple fallback cursor
            cursor = Image.new('RGBA', (10, 10), (255, 255, 255, 200))
            return cursor
    
    def _overlay_cursor(self, screenshot: Image.Image, x: int, y: int) -> Image.Image:
        """
        Overlay cursor image at click coordinates.
        
        Args:
            screenshot: Base screenshot image
            x: Click x coordinate
            y: Click y coordinate
            
        Returns:
            Screenshot with cursor overlaid
        """
        try:
            # Create a copy to avoid modifying original
            result = screenshot.copy()
            
            # Paste cursor at click position (offset to align cursor tip)
            cursor_x = x - 4
            cursor_y = y - 4
            
            # Ensure cursor stays within image bounds
            if cursor_x < 0:
                cursor_x = 0
            if cursor_y < 0:
                cursor_y = 0
            
            # Paste cursor with alpha channel for transparency
            result.paste(self.cursor_image, (cursor_x, cursor_y), self.cursor_image)
            
            return result
            
        except Exception as e:
            print(f"Failed to overlay cursor: {e}")
            return screenshot
    
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
