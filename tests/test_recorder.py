"""
Unit tests for recorder.py - Recorder class.
"""
import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtCore import QObject
from recorder import Recorder
from session_model import TestSession, TestStep


class TestRecorder:
    """Test cases for Recorder class."""
    
    def test_recorder_initialization(self):
        """Test Recorder instantiation."""
        recorder = Recorder()
        
        assert isinstance(recorder, QObject)
        assert recorder.session is None
        assert recorder.is_recording is False
        assert recorder.is_paused is False
        assert recorder.mouse_listener is None
        assert recorder.step_counter == 0
    
    def test_recorder_loads_settings(self):
        """Test that Recorder loads settings on initialization."""
        # Create temporary settings file
        test_settings = {
            "output_dir": "./test_output",
            "auto_capture_on_click": True,
            "capture_delay_ms": 300
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/test_settings.json", 'w') as f:
            json.dump(test_settings, f)
        
        recorder = Recorder("config/test_settings.json")
        
        assert recorder.settings["output_dir"] == "./test_output"
        assert recorder.settings["auto_capture_on_click"] is True
        assert recorder.settings["capture_delay_ms"] == 300
        
        # Cleanup
        os.remove("config/test_settings.json")
    
    def test_recorder_default_settings(self):
        """Test Recorder uses defaults when settings file doesn't exist."""
        recorder = Recorder("config/nonexistent.json")
        
        assert "output_dir" in recorder.settings
        assert "auto_capture_on_click" in recorder.settings
        assert recorder.settings["auto_capture_on_click"] is True
    
    def test_start_recording(self):
        """Test starting a recording session."""
        recorder = Recorder()
        session = TestSession(
            tc_id="TC_REC_001",
            tc_name="Test Recording",
            module="Test",
            environment="SIT",
            tester_name="Tester"
        )
        
        # Mock mouse listener to avoid starting actual global hook
        with patch('recorder.mouse.Listener'):
            result = recorder.start(session)
        
        assert result is True
        assert recorder.is_recording is True
        assert recorder.is_paused is False
        assert recorder.session == session
        assert recorder.step_counter == 0
        assert recorder.session_folder != ""
        assert os.path.exists("temp_sessions")
    
    def test_stop_recording(self):
        """Test stopping a recording session."""
        recorder = Recorder()
        session = TestSession(
            tc_id="TC_REC_002",
            tc_name="Test Stop",
            module="Test",
            environment="SIT",
            tester_name="Tester"
        )
        
        with patch('recorder.mouse.Listener'):
            recorder.start(session)
            returned_session = recorder.stop()
        
        assert recorder.is_recording is False
        assert returned_session is not None
        assert returned_session.end_time is not None
    
    def test_pause_recording(self):
        """Test pausing recording."""
        recorder = Recorder()
        
        recorder.pause()
        
        assert recorder.is_paused is True
    
    def test_resume_recording(self):
        """Test resuming recording."""
        recorder = Recorder()
        recorder.is_paused = True
        
        recorder.resume()
        
        assert recorder.is_paused is False
    
    def test_signal_definitions(self):
        """Test that Recorder has required signals."""
        recorder = Recorder()
        
        # Check signals exist
        assert hasattr(recorder, 'step_captured')
        assert hasattr(recorder, 'error_occurred')
    
    @patch('recorder.mss.mss')
    def test_capture_screen(self, mock_mss):
        """Test screen capture functionality."""
        # Mock mss screenshot
        mock_screenshot = Mock()
        mock_screenshot.width = 1920
        mock_screenshot.height = 1080
        mock_screenshot.rgb = b'\x00' * (1920 * 1080 * 3)
        
        mock_sct_instance = Mock()
        mock_sct_instance.monitors = [{"top": 0, "left": 0, "width": 1920, "height": 1080}]
        mock_sct_instance.grab.return_value = mock_screenshot
        mock_sct_instance.__enter__ = Mock(return_value=mock_sct_instance)
        mock_sct_instance.__exit__ = Mock(return_value=False)
        
        mock_mss.return_value = mock_sct_instance
        
        recorder = Recorder()
        screenshot = recorder._capture_screen()
        
        assert screenshot is not None
        assert screenshot.width == 1920
        assert screenshot.height == 1080
    
    @patch('recorder.ctypes.windll')
    def test_get_active_window_title(self, mock_windll):
        """Test getting active window title."""
        # Mock Windows API calls
        mock_user32 = Mock()
        mock_user32.GetForegroundWindow.return_value = 12345
        mock_user32.GetWindowTextLengthW.return_value = 10
        mock_user32.GetWindowTextW.return_value = 10
        mock_windll.user32 = mock_user32
        
        recorder = Recorder()
        
        with patch('recorder.ctypes.create_unicode_buffer') as mock_buffer:
            mock_buffer.return_value.value = "Test Window"
            title = recorder._get_active_window_title()
        
        # Should not raise exception and return string
        assert isinstance(title, str)
    
    def test_manual_capture_when_not_recording(self):
        """Test manual capture does nothing when not recording."""
        recorder = Recorder()
        
        # Should not raise exception
        recorder.manual_capture()
        
        assert recorder.step_counter == 0
    
    def test_manual_capture_when_paused(self):
        """Test manual capture does nothing when paused."""
        recorder = Recorder()
        recorder.is_recording = True
        recorder.is_paused = True
        
        recorder.manual_capture()
        
        assert recorder.step_counter == 0
    
    def test_session_folder_created(self):
        """Test that session folder is created on start."""
        recorder = Recorder()
        session = TestSession(
            tc_id="TC_REC_003",
            tc_name="Test Folder",
            module="Test",
            environment="SIT",
            tester_name="Tester"
        )
        
        with patch('recorder.mouse.Listener'):
            recorder.start(session)
        
        assert recorder.session_folder != ""
        assert "temp_sessions" in recorder.session_folder
        assert os.path.exists("temp_sessions")
    
    def test_multiple_start_stop_cycles(self):
        """Test multiple start/stop cycles work correctly."""
        recorder = Recorder()
        
        for i in range(3):
            session = TestSession(
                tc_id=f"TC_REC_{i:03d}",
                tc_name=f"Test {i}",
                module="Test",
                environment="SIT",
                tester_name="Tester"
            )
            
            with patch('recorder.mouse.Listener'):
                result = recorder.start(session)
                assert result is True
                assert recorder.is_recording is True
                
                returned_session = recorder.stop()
                assert recorder.is_recording is False
                assert returned_session is not None
