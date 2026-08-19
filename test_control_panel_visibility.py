"""
Manual test script to verify control panel visibility throughout the application lifecycle.
This script helps verify that the control panel remains visible during all operations.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def test_control_panel_visibility():
    """Test control panel visibility throughout operations."""
    print("\n" + "="*70)
    print("CONTROL PANEL VISIBILITY TEST")
    print("="*70)
    print("\nTest Sequence:")
    print("1. Launch application - Control panel should appear")
    print("2. Click 'Start' button - Session dialog appears")
    print("3. Fill session details and click 'Start Recording'")
    print("4. Verify control panel is visible and timer is running")
    print("5. Click anywhere on screen to capture")
    print("6. Verify control panel stays visible during/after capture")
    print("7. Click 'Highlight' button")
    print("8. Verify control panel stays visible after highlight")
    print("9. Click 'Stop & Report'")
    print("10. Verify report generation and control panel returns to initial state")
    print("\n" + "="*70)
    print("\nStarting application...\n")


def main():
    """Run visibility test."""
    # Print test instructions
    test_control_panel_visibility()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("TestTrace Recorder - Visibility Test")
    
    # Apply dark theme
    from main import apply_dark_theme
    apply_dark_theme(app)
    
    # Create main window
    main_window = MainWindow()
    
    # Add a timer to check control panel visibility periodically
    def check_visibility():
        """Periodically check and report control panel visibility."""
        if main_window.control_panel.isVisible():
            print(f"✓ Control Panel VISIBLE - Recording: {main_window.control_panel.is_recording}, "
                  f"Paused: {main_window.control_panel.is_paused}, "
                  f"Steps: {main_window.control_panel.step_count}, "
                  f"Timer: {main_window.control_panel.timer_label.text()}")
        else:
            print(f"✗ Control Panel HIDDEN - This should NOT happen!")
            # Try to restore visibility
            main_window.control_panel.setVisible(True)
            main_window.control_panel.show()
            main_window.control_panel.raise_()
    
    visibility_timer = QTimer()
    visibility_timer.timeout.connect(check_visibility)
    visibility_timer.start(2000)  # Check every 2 seconds
    
    # Show initial status
    print(f"Initial state: Control Panel visible = {main_window.control_panel.isVisible()}")
    print(f"Window flags: {main_window.control_panel.windowFlags()}")
    print(f"Position: ({main_window.control_panel.x()}, {main_window.control_panel.y()})")
    print(f"Size: {main_window.control_panel.width()}x{main_window.control_panel.height()}")
    print("\nMonitoring control panel visibility every 2 seconds...")
    print("Please proceed with testing...\n")
    
    # Run application
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
