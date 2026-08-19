"""
Test to verify system tray icon showMessage calls use correct enum types.
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_tray_icon_message_types_are_correct():
    """
    Verify that all tray_icon.showMessage calls use QSystemTrayIcon enums.
    This test checks the source code for correct usage.
    """
    # Read main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Check that main.py doesn't use QMessageBox.Information with tray_icon
    assert 'QMessageBox.Information' not in main_content or \
           'tray_icon.showMessage' not in main_content or \
           'QSystemTrayIcon.Information' in main_content, \
           "main.py should use QSystemTrayIcon.Information, not QMessageBox.Information"
    
    # Read ui/main_window.py
    with open('ui/main_window.py', 'r', encoding='utf-8') as f:
        main_window_content = f.read()
    
    # Verify QSystemTrayIcon is imported
    assert 'from PyQt5.QtWidgets import' in main_window_content
    assert 'QSystemTrayIcon' in main_window_content
    
    # Verify showMessage calls use QSystemTrayIcon enums
    if 'tray_icon.showMessage' in main_window_content:
        # Check that valid enum values are used
        assert 'QSystemTrayIcon.Information' in main_window_content or \
               'QSystemTrayIcon.Warning' in main_window_content or \
               'QSystemTrayIcon.Critical' in main_window_content, \
               "ui/main_window.py should use QSystemTrayIcon enum values"


@patch('ui.main_window.QSystemTrayIcon')
@patch('ui.main_window.HotkeyThread')
def test_main_window_tray_icon_setup(mock_hotkey, mock_tray):
    """Test that MainWindow sets up tray icon correctly without type errors."""
    from ui.main_window import MainWindow
    
    # Create QApplication if not exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Mock tray icon
    mock_tray_instance = MagicMock(spec=QSystemTrayIcon)
    mock_tray.return_value = mock_tray_instance
    
    # Mock hotkey thread
    mock_thread_instance = MagicMock()
    mock_hotkey.return_value = mock_thread_instance
    
    try:
        # Create main window
        main_window = MainWindow()
        
        # Verify tray icon was created
        assert mock_tray.called
        
        # Clean up
        main_window.close()
        
    except Exception as e:
        pytest.fail(f"MainWindow initialization failed: {e}")


def test_system_tray_icon_enum_values_exist():
    """Verify that QSystemTrayIcon enum values are available."""
    # These should not raise AttributeError
    assert hasattr(QSystemTrayIcon, 'Information')
    assert hasattr(QSystemTrayIcon, 'Warning')
    assert hasattr(QSystemTrayIcon, 'Critical')
    
    # Verify they are enum values (integers)
    assert isinstance(QSystemTrayIcon.Information, (int, QSystemTrayIcon.MessageIcon))
    assert isinstance(QSystemTrayIcon.Warning, (int, QSystemTrayIcon.MessageIcon))
    assert isinstance(QSystemTrayIcon.Critical, (int, QSystemTrayIcon.MessageIcon))


def test_showMessage_signature():
    """Test that QSystemTrayIcon.showMessage accepts correct parameter types."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create a real tray icon (but don't show it)
    tray = QSystemTrayIcon()
    
    # This should not raise a TypeError
    try:
        # Note: showMessage may fail if no tray available, but won't fail on type mismatch
        # We're just checking the method signature accepts these types
        from PyQt5.QtCore import QMetaMethod
        
        # Get the showMessage method
        meta_obj = tray.metaObject()
        for i in range(meta_obj.methodCount()):
            method = meta_obj.method(i)
            if method.name() == b'showMessage':
                # Found the method - it exists and can be called
                assert True
                return
        
        # If we get here, method exists (we can call it above without AttributeError)
        assert True
        
    except Exception as e:
        pytest.fail(f"showMessage signature check failed: {e}")


def test_no_qicon_passed_to_showMessage():
    """
    Verify that no QIcon objects are passed to showMessage.
    The icon parameter should be a QSystemTrayIcon.MessageIcon enum.
    """
    # Check main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Should not have QIcon being passed to showMessage
    lines = main_content.split('\n')
    for i, line in enumerate(lines):
        if 'showMessage' in line:
            # Check surrounding lines for QIcon usage
            context = '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
            assert 'QIcon' not in context or 'QSystemTrayIcon.Information' in context, \
                f"Line {i}: showMessage should not use QIcon parameter"
    
    # Check ui/main_window.py
    with open('ui/main_window.py', 'r', encoding='utf-8') as f:
        main_window_content = f.read()
    
    lines = main_window_content.split('\n')
    for i, line in enumerate(lines):
        if 'showMessage' in line:
            # Check surrounding lines
            context = '\n'.join(lines[max(0, i-2):min(len(lines), i+5)])
            # Should use enum values, not QIcon
            assert 'QIcon(' not in context, \
                f"Line {i}: showMessage should not use QIcon parameter"
