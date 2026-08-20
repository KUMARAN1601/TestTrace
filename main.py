"""
TestTrace Recorder - Main Entry Point

Automated test evidence capture desktop tool for QA engineers.
Captures screenshots, annotations, and generates structured Word reports.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Determine base directory (works for both script and PyInstaller .exe)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add project root to path
sys.path.insert(0, BASE_DIR)

from ui.main_window import MainWindow


def apply_dark_theme(app: QApplication) -> None:
    """
    Apply custom dark theme stylesheet to application.
    
    Args:
        app: QApplication instance
    """
    dark_stylesheet = """
    QWidget {
        background-color: #1B2333;
        color: white;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
    }
    
    QMainWindow {
        background-color: #1B2333;
    }
    
    QDialog {
        background-color: #1B2333;
    }
    
    QLabel {
        color: white;
        background: transparent;
    }
    
    QPushButton {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    
    QPushButton:pressed {
        background-color: #1E40AF;
    }
    
    QPushButton:disabled {
        background-color: #4B5563;
        color: #9CA3AF;
    }
    
    QLineEdit {
        background-color: #232D3F;
        color: white;
        border: 1px solid #2563EB;
        border-radius: 4px;
        padding: 8px;
    }
    
    QLineEdit:focus {
        border: 2px solid #2563EB;
    }
    
    QTextEdit {
        background-color: #232D3F;
        color: white;
        border: 1px solid #2563EB;
        border-radius: 4px;
        padding: 8px;
    }
    
    QComboBox {
        background-color: #232D3F;
        color: white;
        border: 1px solid #2563EB;
        border-radius: 4px;
        padding: 6px;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QComboBox QAbstractItemView {
        background-color: #232D3F;
        color: white;
        selection-background-color: #2563EB;
    }
    
    QTableWidget {
        background-color: #232D3F;
        color: white;
        gridline-color: #374151;
        border: 1px solid #2563EB;
    }
    
    QHeaderView::section {
        background-color: #1B3A6B;
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }
    
    QMessageBox {
        background-color: #1B2333;
    }
    
    QMessageBox QLabel {
        color: white;
    }
    
    QProgressDialog {
        background-color: #1B2333;
    }
    
    QMenu {
        background-color: #232D3F;
        color: white;
        border: 1px solid #2563EB;
    }
    
    QMenu::item:selected {
        background-color: #2563EB;
    }
    """
    
    app.setStyleSheet(dark_stylesheet)


def check_dependencies() -> tuple:
    """
    Check if all required dependencies are installed.
    
    Returns:
        Tuple of (success: bool, missing: list)
    """
    missing = []
    
    required_modules = [
        ('PyQt5', 'PyQt5'),
        ('mss', 'mss'),
        ('PIL', 'Pillow'),
        ('pynput', 'pynput'),
        ('keyboard', 'keyboard'),
        ('docx', 'python-docx'),
    ]
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    return (len(missing) == 0, missing)


def create_required_directories() -> None:
    """Create required application directories if they don't exist."""
    directories = [
        os.path.join(BASE_DIR, 'config'),
        os.path.join(BASE_DIR, 'output'),
        os.path.join(BASE_DIR, 'temp_sessions'),
        os.path.join(BASE_DIR, 'assets')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def main():
    """Main application entry point."""
    # Check dependencies
    success, missing = check_dependencies()
    if not success:
        print("ERROR: Missing required dependencies:")
        for package in missing:
            print(f"  - {package}")
        print("\nPlease install missing packages using:")
        print(f"  pip install {' '.join(missing)}")
        return 1
    
    # Create required directories
    create_required_directories()
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("TestTrace Recorder")
    app.setOrganizationName("TestTrace")
    
    # Apply dark theme
    apply_dark_theme(app)
    
    # Check for admin privileges (recommended for pynput)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("WARNING: Not running as Administrator. "
                  "Global hotkeys may not work properly.")
    except:
        pass
    
    # Create and show main window
    try:
        main_window = MainWindow(base_dir=BASE_DIR)
        
        # Show welcome message
        from PyQt5.QtWidgets import QSystemTrayIcon
        main_window.tray_icon.showMessage(
            "TestTrace Recorder",
            "Application started successfully!\nClick 'New Session' to begin recording.",
            QSystemTrayIcon.Information,
            3000
        )
        
        # Run application
        return app.exec_()
        
    except Exception as e:
        # Show error dialog
        error_msg = f"Failed to start TestTrace Recorder:\n\n{str(e)}"
        QMessageBox.critical(None, "Startup Error", error_msg)
        print(f"ERROR: {error_msg}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
