"""
Integration test for application launch and initialization.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_main_module_imports():
    """Test that main module can be imported without errors."""
    import main
    assert main is not None


def test_main_window_can_be_imported():
    """Test that MainWindow can be imported."""
    from ui.main_window import MainWindow
    assert MainWindow is not None


def test_all_ui_components_import():
    """Test that all UI components can be imported."""
    from ui.control_panel import ControlPanel
    from ui.session_dialog import SessionDialog
    from ui.step_review import StepReviewWindow
    from highlighter import Highlighter
    
    assert ControlPanel is not None
    assert SessionDialog is not None
    assert StepReviewWindow is not None
    assert Highlighter is not None


def test_dependencies_are_available():
    """Test that all required dependencies are available."""
    try:
        import PyQt5
        import mss
        import PIL
        import pynput
        import keyboard
        import docx
        import win32api
        
        assert True
    except ImportError as e:
        pytest.fail(f"Missing dependency: {e}")


def test_check_dependencies_function():
    """Test the dependency check function from main."""
    from main import check_dependencies
    
    success, missing = check_dependencies()
    
    assert success is True
    assert len(missing) == 0


def test_apply_dark_theme_function():
    """Test the dark theme application function."""
    from main import apply_dark_theme
    
    # Create temporary QApplication if not exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Should not raise exception
        apply_dark_theme(app)
        
        # Check that stylesheet was applied
        stylesheet = app.styleSheet()
        assert stylesheet is not None
        assert len(stylesheet) > 0
        assert "#1B2333" in stylesheet  # Background color
        assert "#2563EB" in stylesheet  # Accent color
    finally:
        # Don't quit the app as other tests may need it
        pass


def test_create_required_directories():
    """Test directory creation function."""
    from main import create_required_directories
    
    # Should not raise exception
    create_required_directories()
    
    # Check directories exist
    assert os.path.exists("config")
    assert os.path.exists("output")
    assert os.path.exists("temp_sessions")
    assert os.path.exists("assets")


@patch('ui.main_window.QSystemTrayIcon')
@patch('ui.main_window.HotkeyThread')
def test_main_window_initialization(mock_hotkey, mock_tray):
    """Test that MainWindow can be instantiated."""
    from ui.main_window import MainWindow
    
    # Create QApplication if not exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Mock the hotkey thread start to prevent actual keyboard hooking
    mock_thread_instance = MagicMock()
    mock_hotkey.return_value = mock_thread_instance
    
    try:
        # Create main window
        main_window = MainWindow()
        
        assert main_window is not None
        assert main_window.recorder is not None
        assert main_window.control_panel is not None
        assert main_window.highlighter is not None
        
        # Clean up
        main_window.close()
        
    except Exception as e:
        pytest.fail(f"MainWindow initialization failed: {e}")


def test_settings_file_structure():
    """Test that settings file has correct structure."""
    import json
    
    if os.path.exists("config/settings.json"):
        with open("config/settings.json", 'r') as f:
            settings = json.load(f)
        
        # Check required keys
        assert "output_dir" in settings
        assert "auto_capture_on_click" in settings
        assert "capture_delay_ms" in settings
        assert "hotkey_capture" in settings
        assert "hotkey_stop" in settings
        assert "hotkey_pause" in settings


def test_requirements_file_exists():
    """Test that requirements.txt exists and has content."""
    assert os.path.exists("requirements.txt")
    
    with open("requirements.txt", 'r') as f:
        content = f.read()
    
    # Check for key dependencies
    assert "PyQt5" in content
    assert "mss" in content
    assert "Pillow" in content
    assert "pynput" in content
    assert "python-docx" in content


def test_build_spec_exists():
    """Test that PyInstaller build spec exists."""
    assert os.path.exists("build.spec")
    
    with open("build.spec", 'r') as f:
        content = f.read()
    
    assert "main.py" in content
    assert "TestTrace" in content
